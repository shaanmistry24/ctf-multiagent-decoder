import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reverse_steps(c_code):
    print("Generating plan...")

    #sends marx.c file to gpt4 and gives it prompt
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                     "You are a cybersecurity planner agent designed to analyze C source code from a CTF challenge.\n"
    "Your goal is to reverse-engineer the encoding logic used to obfuscate the flag, and output a precise JSON plan of decoding steps.\n\n"
    "Your output MUST be valid JSON in this format:\n"
    "{\n"
    "  \"steps\": [\n"
    "    {\"step\": 1, \"description\": \"Rotate the byte left by (index % 8).\"},\n"
    "    {\"step\": 2, \"description\": \"Apply bitwise OR of the high nibble with the negated low nibble: (z & 0xF0) | ((~z) & 0x0F).\"},\n"
    "    {\"step\": 3, \"description\": \"Subtract 42 from the result and wrap with & 0xFF.\"},\n"
    "    {\"step\": 4, \"description\": \"Rotate the byte right by ((index + 3) % 7).\"},\n"
    "    {\"step\": 5, \"description\": \"XOR the result with (index * 37) & 0xFF.\"}\n"
    "  ]\n"
    "}\n\n"
    "DO NOT include explanations, commentary, or markdown. Return only valid JSON in this format."
                )
            },
            {
                "role": "user",
                "content": c_code
            }
        ]
    )

    #returns gpt response
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    
    with open("marx.c", "r") as f:
        c_code = f.read()

    steps_text = generate_reverse_steps(c_code)

#strips code block formatting if necessary
if "```json" in steps_text:
    steps_text = steps_text.split("```json")[1].split("```")[0].strip()
elif "```" in steps_text:
    steps_text = steps_text.split("```")[1].split("```")[0].strip()

steps_json = json.loads(steps_text)

    with open("steps.json", "w") as f:
        json.dump(steps_json, f, indent=4)

    print("Saved reverse steps to steps.json")
