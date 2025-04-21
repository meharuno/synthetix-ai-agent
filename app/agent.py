from langchain_ollama import OllamaLLM
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from extractor import extract_booking_info
from dateutil import parser
import re

llm = OllamaLLM(model="mistral")
user_memories = {}      # conversation memory for each user
def get_user_memory(user_id):
    if user_id not in user_memories:
        user_memories[user_id] = ConversationBufferMemory(return_messages=True)
    return user_memories[user_id]

def get_conversation_chain(user_id):    # Create conversation chain per user
    memory = get_user_memory(user_id)
    return ConversationChain(llm=llm, memory=memory)

def get_intent(user_message):  # Intent detection
    lowered = user_message.lower()
    if any(word in lowered for word in ['hi', 'hello', 'hey']):
        return 'greeting'
    elif any(word in lowered for word in ['bye', 'goodbye', 'see you']):
        return 'goodbye'
    elif any(word in lowered for word in ['book', 'appointment', 'schedule']):
        return 'book_appointment'
    elif any(word in lowered for word in ['pay', 'payment']):
        return 'payment_request'
    elif any(word in lowered for word in ['faq', 'help']):
        return 'faq'
    else:
        return 'unknown'

def extract_time_from_message(user_message): # Extract time (To accept time in any format)
    time_pattern = r'(\d{1,2}:\d{2} [apAP][mM]|[apAP][mM] \d{1,2})'
    match = re.search(time_pattern, user_message)
    if match:
        return match.group(0)
    return None

def book_appointment(user_message, user_id="default_user"): # Booking handler
    info = extract_booking_info(user_message)
    print("DEBUG - Extracted Info:", info)

    state = update_conversation_state(user_id, info)

    for key in ["service", "date", "time"]:
        if not state.get(key):
            return f"Sorry, I couldn't find your {key} in the message. Could you please rephrase?"

    return (f"🎉 Great! Your {state['service']} is booked for {state['date']} at {state['time']} "
            f"under the name {state.get('name', 'you')}. Let us know if anything changes! 😊")

def handle_payment(user_message): # Payment and FAQ
    return "Here is your payment link: [Insert Payment Link]"

def handle_faq(user_message):
    faqs = {
        'business hours': 'We are open from 9am to 5pm, Monday through Friday.',
        'contact': 'You can reach us at support@ourcompany.com.',
    }
    for question, answer in faqs.items():
        if question in user_message.lower():
            return answer
    return "Sorry, I couldn't find an answer to that. Can you ask something else?"

def get_ai_response(user_message, user_id="default_user"):  # Central dispatcher
    intent = get_intent(user_message)

    if intent == 'greeting':
        return "Hi there! 👋 How can I assist you today?"
    elif intent == 'goodbye':
        return "Goodbye! 👋 Have a great day!"
    elif intent == 'book_appointment':
        return book_appointment(user_message, user_id=user_id)
    elif intent == 'payment_request':
        return handle_payment(user_message)
    elif intent == 'faq':
        return handle_faq(user_message)
    else:
        conversation = get_conversation_chain(user_id)   # Use LLM fallback for unknowns with memory
        return conversation.predict(input=user_message)
    
conversation_state = {} # State update function
def update_conversation_state(user_id, info):
    global conversation_state
    if user_id not in conversation_state:
        conversation_state[user_id] = {}
    for key, value in info.items():
        if value:
            conversation_state[user_id][key] = value
    return conversation_state[user_id]

if __name__ == "__main__":  
    user_id = "user_001"  
    while True:
        user_message = input("User: ")
        if user_message.lower() in ["exit", "quit"]:
            break
        ai_response = get_ai_response(user_message, user_id)
        print(f"AI: {ai_response}")
