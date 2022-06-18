# List View for aiogram
---

### Model
```python
class Template(SqlAlchemyBase):
    __tablename__ = 'template'

    # You should write this block
    
    class ListMeta:
        __verbose_name__ = 'Шаблон' # Name of element
        __verbose_name_plural__ = 'Шаблоны' # Name of elements

        name = 'название' # description for element property
        text = 'текст'
        image = 'изображение'

    def to_title(self): # function for representation of element
        return self.name.title()
    
    # You should write this block

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    text = Column(String, nullable=False)
    image = Column(String)
```

### Using
```python
from main import db, dp, bot
from aiogram.types import Message
from aiogram_list_view import ListView
from database.models import Template

@dp.message_handler(commands=['templates'])
async def templates(message: Message):
    lv = ListView(Template, db)
    
    # show page
    keyboard = lv.get_page() # get 0'th page
    keyboard = lv.get_page(n) # get n'th page

    # ---------
    template = db.query(Template).first()
    keyboard = lv.get_page_by_id(template.id) # returns page that contains element with id=template.id
    
    await message.answer(text='List of templates', reply_markup=keyboard) 
```

## Contributors
- [@platon-p](https://github.com/platon-p)