from openai import OpenAI
import config

client = OpenAI(
    api_key=config.api_key,
)


async def gpt(message: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ],
        temperature=0,
        max_tokens=2048
    )
    return response.choices[0].message.content
