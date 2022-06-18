from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class ListView:
    model: Base
    db: Session

    def __init__(self, model: Base, db_conn: Session):
        self.model = model
        self.db = db_conn

    def get_page(self, page_num=0) -> InlineKeyboardMarkup:
        items = self.db.query(self.model).all()
        keyboard = InlineKeyboardMarkup()
        for item in items[page_num * 8:page_num * 8 + 8]:
            keyboard.add(
                InlineKeyboardButton(
                    f'{item.id}. {item.to_title()}',
                    callback_data=f'{self.model.__name__}_get_{item.id}'
                )
            )
        if len(items) > 8:
            print(self.model.__name__.lower())
            keyboard.add(
                InlineKeyboardButton(
                    '<-' if page_num > 0 else ' ',
                    callback_data=f'{self.model.__name__}_toPage_{page_num - 1}' if page_num > 0 else 'ignore'),
                InlineKeyboardButton(
                    f'{page_num + 1}/{len(items) // 8 + 1}', callback_data=f'{self.model.__name__}_toPage_0'),
                InlineKeyboardButton(
                    '->' if page_num * 8 + 8 < len(items) else ' ',
                    callback_data=f'{self.model.__name__.lower()}_toPage_{page_num + 1}' if page_num * 8 + 8 < len(
                        items) else 'ignore')
            )
        keyboard.add(
            InlineKeyboardButton(f'✏️ Создать {self.model.ListMeta.__verbose_name__}',
                                 callback_data=f'{self.model.__name__}_create')
        )
        return keyboard

    def get_page_by_id(self, idd: int) -> InlineKeyboardMarkup:
        items = self.db.query(self.model).all()
        if idd == 0:
            return self.get_page(1)
        item_num = 0
        for ind, item in enumerate(items):
            if item.id == idd:
                item_num = ind
                break
        else:
            return self.get_page(1)
        page_num = item_num // 8
        return self.get_page(page_num)

    def get_item_page(self, item_id: int) -> InlineKeyboardMarkup:
        item = self.db.query(self.model).filter(self.model.id == item_id).first()
        if item is None:
            return ReplyKeyboardRemove()
        keyboard = InlineKeyboardMarkup()
        property_names = {k: v for k, v in item.ListMeta.__dict__.items() if not k.startswith('__')}
        for name, value in property_names.items():
            keyboard.add(
                InlineKeyboardButton(
                    f'Изменить {value}',
                    callback_data=f'{self.model.__name__}_edit_{name}_{item.id}'
                )
            )
        return keyboard
