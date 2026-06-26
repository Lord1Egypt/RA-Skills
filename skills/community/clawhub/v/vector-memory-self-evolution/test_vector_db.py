#!/usr/bin/env python3
"""
简化版语义检索测试 - 使用已有向量数据
"""
import chromadb
from pathlib import Path

WORKSPACE = Path.home() / '.openclaw/workspace'
VECTOR_DB_DIR = WORKSPACE / 'vector_db'

def test_vector_db():
    """测试向量库是否可用"""
    print("🧪 向量库测试\n")
    print("=" * 60)
    
    try:
        client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
        collection = client.get_collection("memories")
        
        # 获取集合信息
        count = collection.count()
        print(f"📦 向量库状态:")
        print(f"   位置: {VECTOR_DB_DIR}")
        print(f"   总记录数: {count}")
        
        if count == 0:
            print("\n❌ 向量库为空，请先运行向量化脚本")
            return
        
        # 获取前3条记录
        results = collection.get(limit=3, include=['documents', 'metadatas'])
        
        print(f"\n📝 示例记录:")
        for i, (doc, meta) in enumerate(zip(results['documents'], results['metadatas']), 1):
            print(f"\n【记录 {i}】")
            print(f"   来源: {meta.get('source', '未知')}")
            print(f"   时间: {meta.get('timestamp', '未知')}")
            print(f"   类型: {meta.get('type', '未知')}")
            print(f"   内容: {doc[:100]}{'...' if len(doc) > 100 else ''}")
        
        print("\n" + "=" * 60)
        print("✅ 向量库测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == '__main__':
    test_vector_db()