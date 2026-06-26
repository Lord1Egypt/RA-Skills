#!/usr/bin/env python3
"""
语义检索测试 - 测试向量记忆的语义搜索功能
"""
import chromadb
from pathlib import Path

WORKSPACE = Path.home() / '.openclaw/workspace'
VECTOR_DB_DIR = WORKSPACE / 'vector_db'

def semantic_search(query, n_results=3):
    """语义搜索记忆"""
    print(f"\n🔍 语义搜索: {query}\n")
    print("=" * 60)
    
    try:
        client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
        collection = client.get_collection("memories")
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        if not results['documents'] or not results['documents'][0]:
            print("❌ 未找到相关记忆")
            return
        
        documents = results['documents'][0]
        metadatas = results['metadatas'][0] if results['metadatas'] else [{}] * len(documents)
        distances = results['distances'][0] if results.get('distances') else [0] * len(documents)
        
        for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances), 1):
            print(f"\n【结果 {i}】")
            print(f"📄 来源: {meta.get('source', '未知')}")
            print(f"📅 时间: {meta.get('timestamp', '未知')}")
            print(f"🎯 相似度: {1 - dist:.3f}")
            print(f"📝 内容:")
            print(f"   {doc[:200]}{'...' if len(doc) > 200 else ''}")
            
            if meta.get('type'):
                print(f"   类型: {meta.get('type')}")
            if meta.get('title'):
                print(f"   标题: {meta.get('title')}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"❌ 搜索失败: {e}")

if __name__ == '__main__':
    print("🧪 向量记忆语义检索测试\n")
    
    # 测试多个查询
    test_queries = [
        "如何高效安装 Python 包",
        "npm install 失败怎么办",
        "代码风格规范",
        "自我进化系统",
        "飞书配置"
    ]
    
    for query in test_queries:
        semantic_search(query, n_results=2)
        print("\n")