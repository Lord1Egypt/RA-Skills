# -*- coding: utf-8 -*-
import os
import sys
import requests

api_key = os.environ.get("ALIYUN_API_KEY", "sk-1f3847debc3e492e81f64115b20c6d82")
url = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "text-embedding-v2",
    "input": {
        "texts": ["测试文本"]
    }
}

print("正在调用阿里云 API...")
response = requests.post(url, headers=headers, json=payload, timeout=30)
print(f"状态码：{response.status_code}")

result = response.json()
print(f"返回键：{result.keys()}")

if "output" in result and "embeddings" in result["output"]:
    embedding = result["output"]["embeddings"][0]["embedding"]
    print(f"向量维度：{len(embedding)}")
    print(f"前 10 个值：{embedding[:10]}")
    print("测试成功！")
else:
    print(f"错误：{result}")
