"""IA DEL REY: simple Spanish-language Telegram text utility bot."""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand, KeyboardButton, Message, ReplyKeyboardMarkup

from text_tools import format_text, summarize_text

BOT_NAME = "🤖 IA DEL REY"
BOT_ABOUT = "Herramientas en español para dar formato a textos y crear resúmenes breves."
BOT_DESCRIPTION = (
    "IA DEL REY ofrece herramientas de texto dentro de Telegram. "
    "Elige Mejorar formato para ordenar espacios y signos de puntuación, "
    "o Resumir texto para obtener un resumen extractivo de varias oraciones. "
    "No requiere registros, pagos ni enlaces externos."
)

FORMAT_BUTTON = "✍️ Mejorar formato"
SUMMARY_BUTTON = "📝 Resumir texto"
HELP_BUTTON = "❓ Ayuda"

MAX_INPUT = 3400
WELCOME = (
    "¡Bienvenido a IA DEL REY!\n\n"
    "Herramientas sencillas para trabajar con textos en español.\n\n"
    "✍️ Mejorar formato: organiza espacios y puntuación.\n"
    "📝 Resumir texto: extrae las ideas de varias oraciones.\n"
    "❓ Ayuda: consulta instrucciones.\n\n"
    "Elige una opción del menú para empezar."
)
HELP_TEXT = (
    "Cómo usar IA DEL REY:\n\n"
    "1. Toca «Mejorar formato» y envía un texto. "
    "El bot limpiará espacios y algunos detalles de puntuación; "
    "no es un corrector gramatical completo.\n\n"
    "2. Toca «Resumir texto» y envía al menos tres oraciones. "
    "Se elegirán oraciones relevantes del texto original; "
    "el bot no genera ni verifica hechos nuevos.\n\n"
    "3. Usa /cancel para volver al menú o /start para reiniciar.\n\n"
    "Máximo: 3400 caracteres por texto. No envíes datos confidenciales."
)
MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=FORMAT_BUTTON)],
        [KeyboardButton(text=SUMMARY_BUTTON)],
        [KeyboardButton(text=HELP_BUTTON)],
    ],
    resize_keyboard=True,
    input_field_placeholder="Selecciona una herramienta",
)
dp = Dispatcher()
user_modes: dict[tuple[int, int], str] = {}


def user_key(message: Message) -> tuple[int, int]:
    return (message.chat.id, message.from_user.id if message.from_user else 0)


@dp.message(CommandStart())
async def on_start(message: Message) -> None:
    user_modes.pop(user_key(message), None)
    await message.answer(WELCOME, reply_markup=MENU)


@dp.message(Command("help"))
@dp.message(F.text == HELP_BUTTON)
async def on_help(message: Message) -> None:
    await message.answer(HELP_TEXT, reply_markup=MENU)


@dp.message(Command("cancel"))
async def on_cancel(message: Message) -> None:
    user_modes.pop(user_key(message), None)
    await message.answer("Operación cancelada. Elige una opción del menú.", reply_markup=MENU)


@dp.message(F.text == FORMAT_BUTTON)
async def choose_format(message: Message) -> None:
    user_modes[user_key(message)] = "format"
    await message.answer(
        "Envía el texto que deseas ordenar. Corregiré espacios y algunos signos de puntuación.",
        reply_markup=MENU,
    )


@dp.message(F.text == SUMMARY_BUTTON)
async def choose_summary(message: Message) -> None:
    user_modes[user_key(message)] = "summary"
    await message.answer(
        "Envía un texto en español con al menos tres oraciones para obtener un resumen extractivo.",
        reply_markup=MENU,
    )


@dp.message(F.text.startswith("/"))
async def unknown_command(message: Message) -> None:
    await message.answer("Comando no reconocido. Usa /start o /help.", reply_markup=MENU)


@dp.message(F.text)
async def process_text(message: Message) -> None:
    mode = user_modes.get(user_key(message))
    if mode is None:
        await message.answer("Primero elige una herramienta del menú.", reply_markup=MENU)
        return

    original = (message.text or "").strip()
    if not original:
        await message.answer("Envía un texto que no esté vacío.")
        return
    if len(original) > MAX_INPUT:
        await message.answer(f"El texto supera {MAX_INPUT} caracteres. Envía uno más corto.")
        return

    if mode == "format":
        result = format_text(original)
        await message.answer("Texto con formato:\n\n" + result, reply_markup=MENU)
    else:
        result = summarize_text(original)
        if result is None:
            await message.answer(
                "Para resumir, envía un texto con al menos tres oraciones separadas "
                "por puntos, signos de interrogación o saltos de línea.",
                reply_markup=MENU,
            )
        else:
            await message.answer("Resumen extractivo:\n\n" + result, reply_markup=MENU)


@dp.message()
async def other_content(message: Message) -> None:
    await message.answer("Por favor, envía texto o utiliza los botones del menú.", reply_markup=MENU)


async def configure_profile(bot: Bot) -> None:
    """Update the public BotFather name/About/Description through Bot API."""
    for operation in (
        bot.set_my_name(name=BOT_NAME),
        bot.set_my_short_description(short_description=BOT_ABOUT),
        bot.set_my_description(description=BOT_DESCRIPTION),
        bot.set_my_commands(
            commands=[
                BotCommand(command="start", description="Abrir el menú principal"),
                BotCommand(command="help", description="Consultar instrucciones"),
                BotCommand(command="cancel", description="Cancelar la herramienta actual"),
            ]
        ),
    ):
        try:
            await operation
        except TelegramAPIError:
            logging.exception("Could not update part of the Telegram bot profile")


async def main() -> None:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Missing BOT_TOKEN environment variable")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    bot = Bot(token=token)
    try:
        await configure_profile(bot)
        await bot.delete_webhook(drop_pending_updates=False)
        logging.info("Starting IA DEL REY polling")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
