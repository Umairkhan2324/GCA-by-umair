import getpass
import os
from typing import Dict, Optional
from dotenv import load_dotenv
import signal

load_dotenv()

# Make sure you have OPENAI_API_KEY in your .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

from upsonic import Task, Agent
from upsonic.client.tools import Search

task = Task(
    "Research latest news in Anthropic and OpenAI", 
    tools=[Search]
)

agent = Agent(
    "AI journalist",
    api_key=OPENAI_API_KEY  # Pass the API key to the agent
)

# Running the task
agent.print_do(task)

def async_wrapper(handler):
    if os.name == 'posix':  # Check if the OS is Unix-like
        signal.signal(signal.SIGALRM, handler)
    else:
        print("SIGALRM is not available on this platform.")
        # Handle the case for Windows or other platforms