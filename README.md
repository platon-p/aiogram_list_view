# Inline buttons list view for **aiogram**

## Looks like
![looksLike](images/looksLike.gif)
``` python
chats = [
    "".join(random.sample("abcdefgh", 8)) 
    for _ in range(100)
]
buttons = (
    InlineKeyboardButton(
        "✅ Next",
        callback_data="next"
    ),
    InlineKeyboardButton(
        "⬅ Back",
        callback_data="back"
    )
)
lv = ListView(chats, 2, buttons=buttons)
keyboard = lv.get_page()
lv.register_handlers(dispatcher)
await bot.send_message(
    123456,
    "How ListView looks like",
    reply_markup=keyboard
)
```