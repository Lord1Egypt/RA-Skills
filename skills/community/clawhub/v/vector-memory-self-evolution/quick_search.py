#!/usr/bin/env python3
"""
快速向量检索脚本 - 搜索今天的对话记录
"""
import chromadb
from pathlib import Path

WORKSPACE = Path.home() / '.openclaw/workspace'
VECTOR_DB_DIR = WORKSPACE / 'vector_db'

def search_today(query, n_results=5):
    """搜索今天的对话记录"""
    print(f"\n🔍 向量检索: {query}\n")
    print("=" * 60)

    try:
        client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
        collection = client.get_collection("memories")

        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )

        if not results['documents'] or not results['documents'][0]:
            print("❌ 未找到相关内容")
            return []

        documents = results['documents'][0]
        metadatas = results['metadatas'][0] if results['metadatas'] else [{}] * len(documents)
        distances = results['distances'][0] if results.get('distances') else [0] * len(documents)

        matched_results = []

        for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances), 1):
            # 只显示今天的记录
            if '2026-03-29' in meta.get('source', ''):
                matched_results.append({
                    'content': doc,
                    'source': meta.get('source', '未知'),
                    'type': meta.get('type', '未知'),
                    'timestamp': meta.get('timestamp', '未知'),
                    'similarity': 1 - dist
                })

                print(f"\n【结果 {len(matched_results)}】")
                print(f"📄 来源: {meta.get('source', '未知')}")
                print(f"📅 时间: {meta.get('timestamp', '未知')}")
                print(f"🎯 相似度: {1 - dist:.3f}")
                print(f"📝 内容:")
                print(f"   {doc[:300]}{'...' if len(doc) > 300 else ''}")

        print("\n" + "=" * 60)
        return matched_results

    except Exception as e:
        print(f"❌ 检索失败: {e}")
        return []

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        search_today(query)
    else:
        print("用法: python3 quick_search.py <查询内容>")
        print("示例: python3 quick_search.py 语音插件")