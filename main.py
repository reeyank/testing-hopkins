from fastapi import FastAPI
import requests
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # React or Next.js frontend
    "hopkin-test.vercel.app"
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Can also be ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],     # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],     # Allow all headers
)

gpt_key = os.environ.get("gpt_key")
deepseek_key = os.environ.get("deepseek_key")
gemini_key = os.environ.get("gemini_key")
claude_key = os.environ.get("claude_key")

from pydantic import BaseModel
class Request(BaseModel):
    query: str

@app.post("/")
def read_root(req: Request):
    chatGPT = call_model("gpt", req.query)
    deepseek = call_model("deepseek", req.query)
    # gemini = call_model("gemini", query)
    claude = call_model("claude", req.query)

    return {
        "gpt": chatGPT,
        "deepseek": deepseek,
        # "gemini": gemini,
        "claude": claude
    }

def call_model(model_name: str, query: str):
    if model_name == "gpt":
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {gpt_key}"
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant answering questions for tests."
                },
                {
                    "role": "user",
                    "content": PROMPT.format(query=query)
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        res = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        print(res)
        return res

    elif model_name == "deepseek":
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {deepseek_key}"
        }

        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant answering questions for tests."
                },
                {
                    "role": "user",
                    "content": PROMPT.format(query=query)
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        res = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        print(res)
        return res

    elif model_name == "gemini":
        url = "https://generativelanguage.googleapis.com/v1beta/openai/"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {gemini_key}"
        }

        data = {
            "model": "gemini-2.0-flash",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant answering questions for tests."
                },
                {
                    "role": "user",
                    "content": PROMPT.format(query=query)
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        res = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        print(res)
        return res

    elif model_name == "claude":
        url = "https://api.anthropic.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {claude_key}"
        }

        data = {
            "model": "claude-3-7-sonnet-latest",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant answering questions for tests."
                },
                {
                    "role": "user",
                    "content": PROMPT.format(query=query)
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        print(response)
        res = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        print("claude", res)
        return res

    return "Model not found"

PROMPT = """Answer the following question and choose one of the following answer choices. DO NOT answer with the whole answer, only answer with the NUMBER in which the choice appears in. FOR EXAMPLE, if the correct answer choice is the 3rd one listed, return 3. DO NOT provide any extra information or context.

Question and choices: {query}

BE SURE TO ONLY RETURN A NUMBER!
"""

    