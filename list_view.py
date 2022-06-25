from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram import types, Dispatcher
from typing import Tuple, Union, Callable, List, Iterable


class ListView:
    """
    Сreates a list-like keyboard that allows you to scroll through "pages" with items.
    Developed by: https://github.com/mrskyguy
                  https://github.com/platon-p

    Property "lv_unique_id" is using for unique callback_data name. 
    Callback data which using for ListView will be look like "_ListViewItems{lv_unique_id}" 
    """
    lv_unique_id = 0

    def __init__(
        self, 
        items: Iterable[Union[str, int]], 
        row_width: int = 1, 
        is_enumerate: bool = False,
        buttons: Iterable[InlineKeyboardButton] = []
    ) -> None:
        """
        items - items for display
        row_width - how many items should be displayed in a row
        is_enumerate - should items be enumerated
        buttons - list of buttons which should be displayed below, after ListView's buttons
        """

        self.items = [
            (index, item) 
            for index, item in enumerate(items)
        ]
        self.row_width = row_width
        self.is_enumerate = is_enumerate
        self.buttons = buttons

        ListView.lv_unique_id += 1
        self._lv_unique_id = ListView.lv_unique_id
        self._callback_data_name = f"_ListViewItems{self._lv_unique_id}"
    
    def get_lv_unique_id(self) -> int:
        return self._lv_unique_id
    
    def get_callback_data_name(self) -> str:
        return self._callback_data_name

    def get_page(self, page_num: int = 0) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()

        for ind, item in self.items[page_num * 8 : page_num * 8 + 8]:
            btn = InlineKeyboardButton(
                f"{f'{ind + 1}. ' if self.is_enumerate else ''}{item}",
                callback_data=f'{self._callback_data_name}_get_{ind}'
            )
            if ind % self.row_width == 0:
                keyboard.add(btn)
            else: 
                keyboard.insert(btn)

        if len(self.items) > 8:
            keyboard.add(
                InlineKeyboardButton(
                    '⟵' if page_num > 0 else ' ',
                    callback_data=(
                        f'{self._callback_data_name}_toPage_{page_num - 1}' 
                        if page_num > 0 else 
                        f'{self._callback_data_name}_ignore'
                    )
                ),
                InlineKeyboardButton(
                    f'{page_num + 1}/{len(self.items) // 8 + 1}', 
                    callback_data=f'{self._callback_data_name}_toPage_{0 if page_num != 0 else len(self.items) // 8}'
                ),
                InlineKeyboardButton(
                    '⟶' if (page_num * 8 + 8) < len(self.items) else ' ',
                    callback_data=(
                        f'{self._callback_data_name}_toPage_{page_num + 1}' 
                        if (page_num * 8 + 8) < len(self.items) else 
                        f'{self._callback_data_name}_ignore'
                    )
                )
            )

        for button in self.buttons:
            keyboard.add(button)

        return keyboard

    def get_page_by_id(self, idd: int) -> InlineKeyboardMarkup:
        if idd == 0:
            return self.get_page(1)

        item_num = 0
        for ind, item in self.items:
            if item.id == idd:
                item_num = ind
                break
        else:
            return self.get_page(1)

        page_num = item_num // 8
        return self.get_page(page_num)


    async def to_page(self, callback_query: types.CallbackQuery) -> None:
        page_num = int(callback_query.data.split('_')[-1])
        keyboard = self.get_page(page_num)
        await callback_query.message.edit_reply_markup(keyboard)

    async def get_item_page_handler(self, callback_query: types.CallbackQuery) -> None:
        item_id = int(callback_query.data.split('_')[-1])
        await callback_query.message.edit_text(self.items[item_id][1], reply_markup=None)

    def get_handlers(self) -> List[Tuple[Callable, Callable]]:
        handlers = [
            (
                self.to_page, 
                lambda callback_query: callback_query.data.startswith(
                    f'{self._callback_data_name}_toPage_'
                )
            ),
            (
                self.get_item_page_handler,
                lambda callback_query: callback_query.data.startswith(
                    f'{self._callback_data_name}_get_'
                )
            )
        ]

        return handlers
    
    def register_handlers(self, dp: Dispatcher) -> None:
        for handler in self.get_handlers():
            dp.register_callback_query_handler(*handler)
