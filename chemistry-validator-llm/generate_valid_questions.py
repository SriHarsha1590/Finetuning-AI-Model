import openai
import csv
import sys
import os
import re

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "GAIA"

def qgen(source_text):
    client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a high school chemistry teacher. Respond with 5 questions that can be answered by the text in the user message. Each question must be on the subject of chemical science. The text in the user message must contain specific answers to each question. Each question must be on its own line. Just list the questions without any introductory text or numbers.",
            },
            {
                "role": "user",
                "content": source_text,
            }
        ],
        model=MODEL_NAME,
        stream=False,
    )
    return chat_completion.choices[0].message.content

def main():
    results = [];
    arguments = sys.argv[1:]

    with open(arguments[0], 'r', newline='') as txtfile:
        txt_data = txtfile.read()
        paras = re.split('^\s*$', txt_data, flags=re.MULTILINE) 

        current_line = 0
        for p in paras:
            current_line = current_line + 1
            print(str(current_line) + ' of ' + str(len(paras)))
            print(p + "\n\n\n")
            if len(p.strip()) == 0:
                continue

            qs = qgen(p)
            for q in qs.splitlines():
                if len(q.strip()) == 0 or (not q.endswith("?")):
                    continue
                print('question: ' + q)
                results.append(q.replace("'", "").replace("\"", ""))

    with open(arguments[1], 'w', newline='') as jsonfile:
        for row in results:
            jsonfile.write('{\n')
            jsonfile.write('"instruction": ')
            jsonfile.write('"Determine if the input is a question related to chemical science. If it is, return a JSON object with the \'valid\' field set to true. If it is not, return a JSON object with the \'valid\' field set to false, and the \'reason\' field set to the type of question or statement it is.",\n')
            jsonfile.write('"input": "')
            jsonfile.write(row)
            jsonfile.write('",\n')
            jsonfile.write('"output": "{\'valid\': true}"\n')
            jsonfile.write('},\n')

if __name__ == "__main__":
    main()
