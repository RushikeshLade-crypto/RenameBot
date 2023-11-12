import os
import telebot

# Set up the Telegram bot token
bot = telebot.TeleBot("6760943523:AAE2OdxGWqxMDYH09sPNeipcrRR8Fs47_n0")

# Dictionary to store user's requested file names
user_new_names = {}

# Define the handler for the "/start" command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the file renamer bot. Send me a file to rename it. By @kids_coder") 

# Define the handler for receiving a file
@bot.message_handler(content_types=['document'])
def handle_file(message):
    # Get the file name
    file_name = message.document.file_name

    # Get the file ID
    file_id = message.document.file_id

    # Download the file
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Prompt the user for a new name
    bot.send_message(message.chat.id, f"Current file name: {file_name}\nWhat should be the new name?")

    # Store the user's chat ID for later reference
    user_chat_id = message.chat.id

    # Update the dictionary with the user's request
    user_new_names[user_chat_id] = (file_name, downloaded_file)

# Define a handler for receiving new names
@bot.message_handler(func=lambda message: message.chat.id in user_new_names and user_new_names[message.chat.id] is not None)
def handle_new_name(message):
    # Get the user's requested new name and downloaded file
    original_file_name, downloaded_file = user_new_names[message.chat.id]

    # Get the user's requested new name
    new_name = message.text.strip()

    # Rename the file in memory
    renamed_file_name = "" + new_name
    with open(renamed_file_name, 'wb') as renamed_file:
        renamed_file.write(downloaded_file)

    # Send the renamed file back to the user
    with open(renamed_file_name, 'rb') as renamed_file:
        bot.send_document(message.chat.id, renamed_file)

    # Remove the entry from the dictionary
    del user_new_names[message.chat.id]

    # Delete the temporary file
    os.remove(renamed_file_name)

# Start the bot
bot.polling()
