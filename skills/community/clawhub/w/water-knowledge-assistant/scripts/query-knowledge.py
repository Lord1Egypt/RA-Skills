import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 配置
KNOWLEDGE_BASE_DIR = r"D:\code\openclaw_lakeskill\files"
VECTOR_STORE_DIR = r"D:\code\openclaw_lakeskill\water-knowledge-assistant\vector_store"
EMBEDDING_MODEL = "text-embedding-v1"


def query_knowledge(query, k=3):
    """
    查询知识库
    
    Args:
        query (str): 查询文本
        k (int): 返回结果数量
    
    Returns:
        list: 查询结果列表
    """
    try:
        # 创建嵌入模型
        embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        
        # 加载向量存储
        vector_store = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embeddings)
        
        # 执行查询
        results = vector_store.similarity_search(query, k=k)
        
        return results
    except Exception as e:
        print(f"查询知识库时出错: {e}")
        return []


def main():
    """
    主函数，用于命令行查询
    """
    if len(sys.argv) < 2:
        print("用法: python query-knowledge.py <查询文本>")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    print(f"查询: {query}")
    print("=" * 50)
    
    results = query_knowledge(query, k=3)
    
    if results:
        print(f"找到 {len(results)} 个结果:")
        print("=" * 50)
        for i, result in enumerate(results, 1):
            print(f"\n结果 {i}:")
            print(f"内容: {result.page_content[:200]}...")
            print(f"来源: {result.metadata.get('source', '未知')}")
            print(f"相似度: {result.metadata.get('score', '未知')}")
            print("-" * 30)
    else:
        print("未找到相关结果")


if __name__ == "__main__":
    main()