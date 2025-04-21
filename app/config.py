import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Get the OpenAI key securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
