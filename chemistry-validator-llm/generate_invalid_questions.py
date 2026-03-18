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
                "content": "Respond with 2 to 3 questions related to the news headline in the user message. Each question must be on its own line. Just list the questions without any introductory text or numbers.",
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

def agen(source_text, question):
    client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a content reviewer. Answer very briefly to classify the user question. Potential choices are: politics, religion, other. The context of the question is given as follows:\n" + source_text,
            },
            {
                "role": "user",
                "content": question,
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
                result = []
                result.append(q.replace("'", "").replace("\"", ""))
                a = agen(p, q).strip().strip(".").strip("?").lower()
                print('answer: ' + a)
                result.append(a.replace("'", "").replace("\"", ""))
                results.append(result)

    with open(arguments[1], 'w', newline='') as jsonfile:
        for row in results:
            jsonfile.write('{\n')
            jsonfile.write('"instruction": ')
            jsonfile.write('"Determine if the input is a question related to chemical science. If it is, return a JSON object with the \'valid\' field set to true. If it is not, return a JSON object with the \'valid\' field set to false, and the \'reason\' field set to the type of question or statement it is.",\n')
            jsonfile.write('"input": "')
            jsonfile.write(row[0])
            jsonfile.write('",\n')
            jsonfile.write('"output": "{\'valid\': false, \'reason\': \'')
            jsonfile.write(row[1])
            jsonfile.write('\'}"\n')
            jsonfile.write('},\n')

if __name__ == "__main__":
    main()
