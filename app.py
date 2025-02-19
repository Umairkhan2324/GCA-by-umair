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

from upsonic import Task, Agent, KnowledgeBase, ObjectResponse
from upsonic.client.tools import Search, ComputerUse

class initial_repsonse(ObjectResponse):
    analysis : str

class job_list(ObjectResponse):
    jobs : list

my_resume = KnowledgeBase(
    files = ["my_resume.pdf"]
)
Initial_analysis = Task(
    "You are acting as a recruiter and going to deeply analyze and understand resume given in knowledge base and tell which job will be best for this person and will write about what type of jobs with what specifications will be best for him", 
    context = [my_resume],
    response_format = initial_repsonse
)
job_search = Task(
    "You are going to understand the analysis given by task1 and search for the most suited jobs according to it across multiple platfroms.",
    context = [my_resume,Initial_analysis],
    tool = [Search,ComputerUse],
    response_format = job_list
)

agent = Agent(
    "you are job searcher for me and shall find the best jobs out there for me ",
    api_key=OPENAI_API_KEY ,
    model="openai/gpt-4o" # Pass the API key to the agent
)

# Running the task
agent.print_do(job_search)

def async_wrapper(handler):
    if os.name == 'posix':  # Check if the OS is Unix-like
        signal.signal(signal.SIGALRM, handler)
    else:
        print("SIGALRM is not available on this platform.")
        # Handle the case for Windows or other platforms