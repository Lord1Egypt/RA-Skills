from openai import OpenAI

client = OpenAI(
    api_key='sk-1f3847debc3e492e81f64115b20c6d82',
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
)

try:
    response = client.embeddings.create(
        model='text-embedding-v3',
        input=['测试向量搜索']
    )
    embedding = response.data[0].embedding
    print(f"[OK] 阿里云 Embedding API 调用成功！")
    print(f"向量维度：{len(embedding)}")
    print(f"向量前 5 个值：{embedding[:5]}")
except Exception as e:
    print(f"[ERROR] API 调用失败：{e}")
