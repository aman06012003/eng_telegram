from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import pathlib
import textwrap
import google.generativeai as genai

genai.configure(api_key='AIzaSyAytkzRS0Xp0pCyo6WqKJ4m1o330bF-gPk')

model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

import docx2txt

file_path = pathlib.Path('English_Curriculum_Lesson_Objectives.docx')
content = docx2txt.process(file_path)


# 8126949340:AAGmr4ByOLlYXtEQuleOsinS2w_wUogldj0
TOKEN = '8126949340:AAGmr4ByOLlYXtEQuleOsinS2w_wUogldj0'
BOT_USERNAME = '@eng122_bot'



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi there!👋I'm ready to answer your questions. Ask me anything!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am a Test bot. Please type something so I can respond!")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!")


def handle_response(prompt:str) ->str:
    processed: str = prompt.lower()
    flag = model.generate_content(["If "+prompt+" is related to anything like LGBTQ+, mention of homosexuality, politics, war news, crimes, etc. return '1' else return '0'"])
        # st.write(flag.text)
    if '1' in str(flag.text):
            response = "I am a parenting and educational assistance bot. I am unable to answer these questions. Please ask questions related to educational assistance."
    elif '0' in str(flag.text):            
        # context_truncated = textwrap.shorten(content, width=1000)
        response1 = model.generate_content(["""You are an advanced English tutor chatbot designed to help users improve their English language skills interactively. Your goal is to enhance their vocabulary, grammar, reading comprehension, and speaking abilities while providing short, precise, and personalized responses. Adapt your teaching style to the user’s skill level (Beginner, Intermediate, Advanced) and their specific learning objectives.

Chatbot Interaction Guidelines:
Initial Setup:

Start by asking:
"What’s your current English proficiency level? (Beginner, Intermediate, Advanced)"
"What are your learning goals? (e.g., vocabulary, grammar, reading, speaking, exam preparation)"
Interactive Lessons:

Offer tailored lessons based on the user’s responses:
Beginner: "Let’s start with basics. Can you tell me the plural form of 'dog'?"
Intermediate: "What’s the difference between 'few' and 'a few'? Let me know your thoughts."
Advanced: "Explain the difference between 'complement' and 'compliment' with examples."
Provide instant corrections or enhancements based on the user's inputs.
Quizzes and Feedback:

Deliver short, engaging quizzes in real-time:
"Fill in the blank: 'She ___ (run) every morning.' (runs/running/run)"
"Choose the correct word: 'The news ___ interesting. (is/are)'"
Offer immediate feedback:
"Correct! 'She runs' is the right answer because the subject is singular."
"Almost there! Remember, 'news' is singular, so we use 'is.'"
Speaking Practice (Optional):

Simulate conversations: "Let’s practice! Pretend you’re ordering coffee. Type: 'I’d like a cappuccino, please.'"
Provide feedback on sentence structure and suggest alternatives for natural phrasing.
Adaptability:

Adjust responses dynamically based on user inputs.
Celebrate achievements: "Great job! You’ve mastered irregular verbs. Shall we try some advanced vocabulary next?"
Follow-Up Suggestions:

Offer suggestions at the end of sessions:
"Would you like to practice reading comprehension next?"
"Should we focus on common idioms and phrases?"
Example Chat Flow:
Bot: Hi! I’m your English tutor. Let’s start by figuring out where you are. What’s your current English level? (Beginner, Intermediate, Advanced)

User: Beginner.

Bot: Great! What would you like to focus on? Vocabulary, grammar, or something else?

User: Vocabulary.

Bot: Perfect! Let’s start with animals. What’s the plural form of 'cat'?

User: Cats.

Bot: Excellent! That’s correct. Now, try this: What’s the plural form of 'mouse'?""",
f"Question: {prompt}",
f"Context: {content}"])
        
        response = f"{response1.text}"
    else:
        response = "I'm sorry, can you please try rephrasing your question?"
    return response


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    # Your message handling logic goes here
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # if message_type=='group':
    #     if BOT_USERNAME in text:
    #         new_text: str = text.replace(BOT_USERNAME,'').strip()
    #         response: str = handle_response(new_text)
    #     else:
    #         return
    # else:
    response:str=handle_response(text)
    print('BOT:',response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == '__main__':
    print('Starting bot ...')
    app = Application.builder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Register message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    PORT = int(os.environ.get('PORT', '8443'))
    # Register error handler
    app.add_error_handler(error)

    # Start polling
    print("Polling...")
    app.run_polling(poll_interval=10)



