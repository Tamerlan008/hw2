from aiogram import Bot, Dispatcher, types, executor
from config import token
from logging import basicConfig, INFO


basicConfig(level=INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)

start_buttons = [
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Товары'),
    types.KeyboardButton('Заказать'),
    types.KeyboardButton('Контакты')
]

start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

products = {
    '14': {
        'name': 'Iphone 14 pro max',
        'description': '512гб, Цена - 125,000 сом, Цвет - фиолетовый, Артикул - 14',
        'photo': 'https://gsmarena.by/upload/medialibrary/90e/90ea01b9b03cd15a5843fa03f492f6aa.png'
    },
    '45': {
        'name': 'Redmi note 11 pro plus 5G',
        'description': '256гб, Цена - 30,000 сом, Цвет - серый, Артикул - 45',
        'photo': 'https://i02.appmifile.com/200_operator_sg/28/02/2022/6572a6314294e308e09ef8e4cb90bcfd.jpg'
    },
    '67': {
        'name': 'POCO X6 pro',
        'description': '512гб, Цена - 35,000 сом, Цвет - черный, Артикул - 67',
        'photo': 'https://ir.ozone.ru/s3/multimedia-w/c1000/6901060172.jpg'
    }
}

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.full_name}!', reply_markup=start_keyboard)

@dp.message_handler(text='О нас')
async def about_us(message: types.Message):
    await message.answer("Tehno_Shop - онлайн магазин, в котором продают телефоны и т.д.")

@dp.message_handler(text='Контакты')
async def send_contact(message: types.Message):
    await message.answer("+996 995 626 290")
    await message.answer("+996 998 590 052")

product_buttons = [
    types.KeyboardButton("Iphone"),
    types.KeyboardButton("Redmi"),
    types.KeyboardButton("POCO"),
    types.KeyboardButton("Назад")
]

product_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*product_buttons)

@dp.message_handler(text='Товары')
async def show_products(message: types.Message):
    await message.answer("Вот наши товары:", reply_markup=product_keyboard)

@dp.message_handler(text=['Iphone', 'Redmi', 'POCO'])
async def show_product_details(message: types.Message):
    if message.text == 'Iphone':
        product = products['14']
    elif message.text == 'Redmi':
        product = products['45']
    elif message.text == 'POCO':
        product = products['67']
    
    await message.answer_photo(product['photo'])
    await message.answer(f"{product['name']}, {product['description']}")

@dp.message_handler(text='Назад')
async def go_back(message: types.Message):
    await start(message)

@dp.message_handler(text='Заказать')
async def order_product(message: types.Message):
    await message.reply("Введите артикул товара, который хотите заказать:")

@dp.message_handler(lambda message: message.text.isdigit())
async def process_article(message: types.Message):
    article = message.text
    if article in products:
        product = products[article]
        await message.answer_photo(product['photo'])
        await message.answer(f"{product['name']}, {product['description']}")
        await message.answer("Поделитесь вашим контактом, нажав на кнопку 'Поделиться контактом'.",
                             reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
                                 types.KeyboardButton(text="Поделиться контактом", request_contact=True)
                             ))
    else:
        await message.answer("Извините, товар с таким артикулом не найден. Пожалуйста, введите корректный артикул.")

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def process_contact(message: types.Message):
    contact = message.contact
    if not contact:
        await message.answer("Ошибка: Пожалуйста, поделитесь вашим контактом.")
        return

    order_message = (
        f"Новый заказ!\n"
        f"Имя: {contact.first_name} {contact.last_name or ''}\n"
        f"Контакт: {contact.phone_number}"
    )
    async for msg in bot.iter_history(message.chat.id, limit=2):
        if msg.text.isdigit():
            article = msg.text
            product = products.get(article)
            if product:
                order_message += f"\nАртикул товара: {article}\nНазвание товара: {product['name']}"
                break
    
    await bot.send_message(chat_id="-4269502098", text=order_message)
    await message.reply("Спасибо за заказ! Мы свяжемся с вами в ближайшее время.")

executor.start_polling(dp, skip_updates=True)

 

   