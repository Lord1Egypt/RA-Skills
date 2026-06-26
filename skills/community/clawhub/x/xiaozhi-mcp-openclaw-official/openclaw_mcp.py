from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("龙虾机器人")

OPENAI_BASE = os.environ.get('OPENAI_BASE', 'https://openclaw.994938.xyz/v1')
OPENAI_KEY = os.environ.get('OPENAI_KEY', '')
MODEL = os.environ.get('MODEL', 'gpt-5.4')
TIMEOUT = int(os.environ.get('TIMEOUT', '60'))
SYSTEM_PROMPT = os.environ.get('SYSTEM_PROMPT', '你是通过小智 MCP 调用的龙虾机器人，请返回简洁、适合语音播报的中文结果。')

@mcp.tool()
def openclaw_query(message: str) -> str:
    """
    龙虾机器人专用工具。
    当用户提到“龙虾机器人”“龙虾”，或者需要联网查询、复杂分析、外部能力时，调用这个工具。

    参数：
    - message: 要交给龙虾机器人处理的完整问题
    """
    headers = {
        'Authorization': f'Bearer {OPENAI_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': MODEL,
        'messages': [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': message}
        ],
        'max_tokens': 512,
        'temperature': 0.7
    }

    try:
        r = requests.post(f'{OPENAI_BASE}/chat/completions', headers=headers, json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        reply = data['choices'][0]['message']['content']
        return reply.strip() if reply else '龙虾机器人暂时没有生成回复。'
    except Exception as e:
        return f'龙虾机器人暂时连接不上后端服务，请稍后再试。错误：{str(e)}'

if __name__ == '__main__':
    mcp.run(transport='stdio')
