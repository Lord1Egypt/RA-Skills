import asyncio
import os
import aiohttp
from dotenv import load_dotenv
load_dotenv()

DASHSCOPE_KEY = os.getenv("DASHSCOPE_API_KEY")

async def test():
    print("=" * 50)
    print("【测试3】DashScope LLM API")
    print("=" * 50)
    
    # DashScope OpenAI兼容模式
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen-plus",
        "messages": [{"role": "user", "content": "请用一句话介绍北京"}]
    }
    
    print("请求URL:", url)
    print("API Key:", DASHSCOPE_KEY[:10] + "...")
    print("模型:", "qwen-plus")
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data, timeout=30) as resp:
            print("状态码:", resp.status)
            result = await resp.text()
            print("返回数据:", result[:1000])
            
            # 尝试MiniMax
            print("\n" + "=" * 50)
            print("【测试4】MiniMax API（备用）")
            print("=" * 50)
            
            url2 = "https://api.minimax.chat/v1/chat/completions"
            data2 = {
                "model": "MiniMax-M2.5",
                "messages": [{"role": "user", "content": "你好"}]
            }
            
            async with session.post(url2, headers=headers, json=data2, timeout=30) as resp2:
                print("状态码:", resp2.status)
                result2 = await resp2.text()
                print("返回数据:", result2[:500])

if __name__ == "__main__":
    asyncio.run(test())