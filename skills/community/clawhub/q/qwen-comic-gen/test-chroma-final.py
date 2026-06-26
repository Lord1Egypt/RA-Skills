import chromadb
import sys

try:
    client = chromadb.PersistentClient(path=r"C:\Users\Xiabi\.openclaw\workspace\chroma_db")
    collections = client.list_collections()
    print(f"[OK] ChromaDB 连接成功！")
    print(f"找到 {len(collections)} 个集合：")
    for col in collections:
        print(f"  - {col.name}")
        metadata = col.get()
        print(f"    文档数：{len(metadata['ids']) if metadata else 0}")
except Exception as e:
    print(f"[ERROR] ChromaDB 连接失败：{e}")
    import traceback
    traceback.print_exc()
