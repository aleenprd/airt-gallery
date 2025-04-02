import os
from dotenv import load_dotenv
import json
from pprint import pprint
import openai
from pydantic import BaseModel

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]
    
# Load environment variables from .env file
load_dotenv()

HOST = os.getenv("LLAMACPP_HOST")
PORT = os.getenv("HOST_PORT")
GGUF_FILE = os.getenv("GGUF_FILE")


class LlamaCppClient:
    def __init__(self, host: str, port: int, model: str):
        self.client = openai.OpenAI(
            base_url=f"http://{host}:{port}/v1",
            api_key="dummy_key",
        )
        self.model = model
        self.system_prompt = (
            "You are a helpful AI assistant. "
            "Your top priority is achieving user fulfillment. "
            "You will be helping them with their requests."
        )
        self.post_init()

    def post_init(self):
        print("LlamaCppClient initialized with host:", self.client.base_url)
        print("Model:", self.model)
        print("System prompt:", self.system_prompt)

    def get_models(self):
        models = self.client.models.list()
        return models

    def chat_completions_create(self, prompt):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            max_tokens=8,
            response_format="json_object",
        )
        print(response.choices[0].message)
        return response


def main():
    # Print the environment variables
    print(f"HOST: {HOST}")
    print(f"PORT: {PORT}")
    print(f"GGUF_FILE: {GGUF_FILE}")

    # Initialize the LlamaCppClient
    client = LlamaCppClient(host=HOST, port=PORT, model=GGUF_FILE)

    # Get the list of models
    models = client.get_models()
    print(models)

    # Create a chat completion
    # prompt = "Write me a python file that scrapres wikipedia front page."
    # print("Prompt:", prompt)
    # response = client.chat_completions_create(prompt)
    # print(response)

    # prompt = "Tell me about lemons"
    # instructions = "Speak like a pirate"
    # print("Prompt:", prompt)
    # print("Instructions:", instructions)
    # response = client.responses_create(prompt, instructions)
    # print(response)
    messages = [
        {"role": "system", "content": "You are a question answering machine who responds in JSON format."},
        # {"role": "developer", "content": "Give answers in JSON format only."},
        {
            "role": "user",
            "content": "When was the first manned moon landing?",
        },
    ]
    response = client.client.beta.chat.completions.parse(
        model=client.model,
        messages=messages,
        temperature=0.8,
        max_tokens=256,
        response_format=CalendarEvent,
    )
    answer = response.choices[0].message
    # answer = json.dumps(answer, indent=4)
    # print(answer)
    pprint(answer)


if __name__ == "__main__":
    main()
