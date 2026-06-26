import os
import json
from openai import OpenAI

# 读取配置文件
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

client = OpenAI(
    api_key=config["llm"]["api_key"],
    base_url=config["llm"]["base_url"])

def AI(content):
    response = client.chat.completions.create(
        model=config["llm"]["model"],
        messages=[
            {"role": "system", "content": "你是一个天气专家，你要为用户提供针对天气情况的温馨提示。不要使用markdown格式，直接给出1.2.3.的提示内容（三条即可，要标序号），每一个提示之间空一行，要求每条提示都简短有用（每条建议不得超过30字）。天气情况："+str(content)},
            {"role": "user", "content": content},
        ],
        stream=False,
        reasoning_effort="low",
        extra_body={"thinking": {"type": "disabled"}}
    )
    return response.choices[0].message.content