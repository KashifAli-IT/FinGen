import gradio as gr
from groq import Groq
import os
import re

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)

def detect_language(text):
    """Rudimentary language detector for Urdu, Roman Urdu, and English."""
    urdu_chars = re.compile(r"[\u0600-\u06FF]")  # Unicode range for Urdu script

    if urdu_chars.search(text):
        return "urdu"
    
    roman_urdu_keywords = ["mujhe", "kyun", "kaise", "nahi", "hain", "karna", "batao", "kya", "acha", "theek", "mehnga"]
    if any(word in text.lower() for word in roman_urdu_keywords):
        return "roman_urdu"
    
    return "english"

def get_system_prompt(lang):
    if lang == "urdu":
        return (
            "آپ FinGenius ہیں، ایک دوستانہ مالی منصوبہ بندی کا معاون جو پاکستان کے نوجوانوں کی مالی رہنمائی کرتا ہے۔ "
            "ہمیشہ صرف اردو میں جواب دیں۔ بجٹ بنانے، بچت کرنے، اور بنیادی سرمایہ کاری کے بارے میں سادہ مشورے دیں۔"
        )
    elif lang == "roman_urdu":
        return (
            "Aap FinGenius hain, aik friendly financial planner jo Pakistan ke logon ki madad karta hai. "
            "Hamesha sirf Roman Urdu mein jawab dein. Budgeting tips, saving ideas aur tax estimates Roman Urdu mein explain karein."
        )
    else:  # English
        return (
            "You are FinGenius, a friendly financial planning assistant for young people in Pakistan. "
            "Always respond in English only. Provide budgeting advice, saving tips, and basic investment suggestions. "
            "Avoid using any non-English language or mixed-language replies."
        )

def chat_with_memory_auto_language(user_input, history):
    if history is None:
        history = []

    lang = detect_language(user_input)
    system_prompt = get_system_prompt(lang)

    messages = [{"role": "system", "content": system_prompt}] + history
    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        bot_reply = response.choices[0].message.content.strip()
    except Exception as e:
        bot_reply = f"❌ Error: {str(e)}"

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": bot_reply})

    return history, history, ""


"""
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)

def chat_with_memory_english(user_input, history):
    system_prompt = (
        "You are FinGenius, a friendly financial planning assistant for young people in Pakistan. "
        "Always respond in English only. Provide budgeting advice, saving tips, and basic investment suggestions. "
        "Avoid using any non-English language or mixed-language replies."
    )

    if history is None:
        history = []

    messages = [{"role": "system", "content": system_prompt}] + history
    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        bot_reply = response.choices[0].message.content.strip()
    except Exception as e:
        bot_reply = f"❌ Error: {str(e)}"

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": bot_reply})

    return history, history, ""

"""

def launch_fin_genius():
    with gr.Blocks(css="""
    body {
        background-color: #f3f3f3;
        font-family: 'Segoe UI', sans-serif;
    }
    .container {
        max-width: 700px;
        margin: 0 auto;
        padding-top: 40px;
    }
    gr-chatbot {
        border: 1px solid #ddd !important;
        border-radius: 14px !important;
        background: #ffffff !important;
    }
    gr-button {
        background: #28a745 !important;
        color: white !important;
        border-radius: 8px !important;
    }
    gr-textbox {
        border: 1px solid #bbb !important;
    }
    """) as demo:
        with gr.Column(elem_classes="container"):
            gr.Markdown("<h2 style='text-align:center;'>💸 FinGenius – Financial Planner for Pakistan</h2>")
            chatbot = gr.Chatbot(height=400, type="messages", show_copy_button=True)
            state = gr.State([])

            with gr.Row():
                txt = gr.Textbox(
                    placeholder="Enter your question in English...",
                    show_label=False,
                    lines=2
                )
                submit = gr.Button("Send")
"""
            submit.click(
                fn=chat_with_memory_english,
                inputs=[txt, state],
                outputs=[chatbot, state, txt]
            )  """

            submit.click(
                fn=chat_with_memory_auto_language,
                inputs=[txt, state],
                outputs=[chatbot, state, txt]
            )

    return demo
