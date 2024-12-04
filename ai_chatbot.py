import logging
import openai
from decouple import config
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Load OpenAI API key from .env
client = openai.OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=config("api_key_chatgpt")
)

# Enable logging for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle text messages and provide AI-generated feedback
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text  # Get the text message from the user
    
    # Check if the message starts with .bcl
    if user_input.startswith(".bcl"):
        user_input = user_input[3:].strip()
        try:
            # Request feedback from the AI model
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "",
                    },
                    {
                        "role": "user",
                        "content": f"{user_input}",
                    }
                ],
                model="gpt-4o-mini",
                temperature=1,
                max_tokens=4096,
                top_p=1
            )

            # Extract the AI's response from the API response
            ai_feedback = response.choices[0].message.content

            # Send the feedback back to the user
            await update.message.reply_text(f"🤖🤖🤖🤖🤖\n: {ai_feedback}")

        except Exception as e:
            logger.error(f"Error interacting with OpenAI API: {e}")
            await update.message.reply_text("Sorry, I couldn't process your request. Please try again later.")

# Main function to set up the bot
def main():
    # Replace 'your_telegram_bot_token' with your actual Telegram bot token
    token = config("tg_api")
    application = Application.builder().token(token).build()

    # Message handler to process text messages starting with .bcl and generate AI feedback
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
