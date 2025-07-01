import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#ensures there is only raw python code
def extract_code_block(text):
    if "```python" in text:
        return text.split("```python")[1].split("```")[0].strip()
    elif "```" in text:
        return text.split("```")[1].split("```")[0].strip()
    return text.strip()

def load_marx():
    with open("marx.c", "r") as f:
        return f.read()

def load_steps():
    with open("steps.json", "r") as f:
        return json.load(f)

def generate_code(c_source, decoding_steps):
    print("Generating Python script from steps...")

    #sends marx c code and steps to gpt4 and gives it prompt
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    """You are an expert reverse engineer.
You will be given:
1. A C source file used in a CTF challenge.
2. A JSON-formatted list of decoding steps to reverse the encoding logic.

Your task is to generate a fully working Python script that:
- Extracts the obfuscated flag byte array (e.g., gnmupmhiaosg[] or similar).
- Reverses the transformations applied in the original C source, exactly as described.
- Reconstructs the original flag and prints it using: print('The flag is:', flag)

IMPORTANT IMPLEMENTATION RULES:
- DO NOT use input() or manual input from the user.
- DO NOT use placeholders like [] or 'your_flag_here'.
- DO NOT reverse the array if the original C loop encoded forward.
- Use clear and executable Python 3 code.
- Output ONLY valid Python code in a code block.

Recreate the following exact structure and logic for decoding:
1. Implement `rol(j, h)` and `ror(j, h)` functions for left/right bit rotation using `& 0xFF` masking.
2. Loop through the obfuscated array using `for i in range(len(...))`, not reversed.
3. In the loop, apply these transformations in order:
   a. rol the byte by `i % 8`
   b. mask it: `(z & 0xF0) | ((~z) & 0x0F)`
   c. subtract 42 and mask with `& 0xFF`
   d. ror by `(i + 3) % 7`
   e. xor with `(i * 37) & 0xFF`
4. Convert each result to a character using `chr()` and append to the flag.
5. At the end, join the flag characters and print them."""
                )
            },
            {
                "role": "user",
                "content": (
                    f"Here is the original C code:\n\n"
                    f"{c_source}\n\n"
                    f"Here is the plan (JSON):\n\n"
                    f"{json.dumps(decoding_steps, indent=2)}\n\n"
                    "Now generate the Python script"
                )
            }
        ]
    )

    return extract_code_block(response.choices[0].message.content)

c_source = load_marx()
decoding_steps = load_steps()
script = generate_code(c_source, decoding_steps)

#creates file and adds generated script to it
with open("solve_ctf.py", "w") as f:
    f.write(script)

print("Saved solve_ctf.py")

