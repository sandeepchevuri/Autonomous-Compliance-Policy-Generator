import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Shared LLM configuration
LLM = ChatOpenAI(
    model="gpt-5-mini-2025-08-07",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Workspace directory
WORKSPACE_DIR =str(Path(__file__).parent.parent / "workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

# Create subdirectories
SUBDIRS = [
    "research",
    "policies",
    "reviews",
    "audits",
    "summaries",
    "archive"
]

for subdir in SUBDIRS:
    os.makedirs(os.path.join(WORKSPACE_DIR, subdir), exist_ok=True)