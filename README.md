# IA DEL REY

A Spanish Telegram text utility bot with exactly three menu buttons:

- **Mejorar formato**: clean duplicate spaces and basic punctuation.
- **Resumir texto**: select relevant original sentences from a text with three or more sentences.
- **Ayuda**: explain how to use the bot.

The summary is extractive and offline. It is not a generative AI service or a complete grammar checker. It has no external redirects, login prompts, or payments.

## Setup

1. Create a bot with @BotFather. Choose and register a username.
2. Set the environment variable `BOT_TOKEN` to the token from BotFather. Do not save this token in GitHub.
3. Install packages with `python -m pip install -r requirements.txt`.
4. Start locally with `python main.py`.

At startup, the code sets the bot's **name**, **About** (short description), **Description**, and the /start, /help, and /cancel commands using the Telegram Bot API. Confirm those details in BotFather after first deployment. The bot also checks whether its public profile photo is missing and uploads an original IA DEL REY avatar automatically if needed.

**Profile photo:** The bot automatically creates and uploads an original avatar if its profile has no photo. If Telegram denies the update, use BotFather → Edit Bot → Edit Botpic as a fallback. Existing photos are not overwritten.

## Render deployment

Import this repository as a Render Blueprint using `render.yaml` or create a **Background Worker** from the Dockerfile. Add `BOT_TOKEN` as a secret environment variable. Background workers may require a paid plan.

Run one worker only. Running multiple pollers for the same bot token can trigger `getUpdates` conflicts.

## BotFather profile

**Name:** 🤖 IA DEL REY

**About:** Herramientas en español para dar formato a textos y crear resúmenes breves.

**Description:** IA DEL REY ofrece herramientas de texto dentro de Telegram. Elige Mejorar formato para ordenar espacios y signos de puntuación, o Resumir texto para obtener un resumen extractivo de varias oraciones. No requiere registros, pagos ni enlaces externos.

These strings are defined in `main.py` and synchronized automatically when the bot launches.

## Suggested Telegram ad

**Title:** IA DEL REY

**Text:** Da formato a tus mensajes y obtén resúmenes breves de textos en español. Usa las herramientas de IA DEL REY directamente en Telegram.

**URL:** t.me/<your-registered-bot-username> (replace after creating the bot).

Target Spanish-language channels only. Test /start, /help, /cancel, formatting and summarization on mobile and desktop before submitting. Telegram approval is not guaranteed.
