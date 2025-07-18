from openai import OpenAI

client = OpenAI(
    api_key = "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"
)

completion = client.chat.completions.create(
    model ="gpt-3.5-turbo",
    messages=[
        {"role":"system","content":"you are a virtual assistant named jarvis skilled in general task like Alexa and google cloud"},
        {"role":"user","content":"what is coding"}

    ]
)
print(completion.choices[0].message.content)