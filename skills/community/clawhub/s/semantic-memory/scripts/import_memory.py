#!/usr/bin/env python3
"""
记忆导入脚本 — Semantic Memory
将 .md 文件批量导入 ChromaDB 向量数据库
用法：python3 import_memory.py [目录路径] [collection名] [agent名]
默认：当前目录 → memories → 默认Agent
"""
import chromadb, os, sys, time
from datetime import datetime

# ── 配置 ──────────────────────────────────────────────────────────
CLIENT_HOST = os.environ.get('CHROMA_HOST', 'localhost')
CLIENT_PORT = int(os.environ.get('CHROMA_PORT', '8000'))
DB_PATH     = os.environ.get('CHROMA_PATH', './vector_db')

client = chromadb.HttpClient(host=CLIENT_HOST, port=CLIENT_PORT)

# ── 工具函数 ──────────────────────────────────────────────────────
def read_file(path):
    for enc in ('utf-8', 'gbk', 'gb2312', 'latin1'):
        try:
            with open(path, encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    print(f"  ⚠️  无法读取（编码问题）：{path}")
    return None

def slug(name):
    return ''.join(c if c.isalnum() else '_' for c in name)[:40]

def ensure_collection(name):
    try:
        return client.get_collection(name)
    except Exception:
        return client.create_collection(name, metadata={'description': f'Semantic Memory collection: {name}'})

# ── 主导入逻辑 ────────────────────────────────────────────────────
def import_file(file_path, collection_name, agent_name='Semantic Memory'):
    """导入单个 .md 文件到指定 collection"""
    content = read_file(file_path)
    if not content:
        return False

    # 从文件名提取标题（去掉.md）
    title = os.path.splitext(os.path.basename(file_path))[0]

    # metadata
    meta = {
        'source': title,
        'agent':  agent_name,
        'type':   'memory',
        'date':   datetime.now().strftime('%Y-%m-%d'),
        'path':   os.path.abspath(file_path),
    }

    col = ensure_collection(collection_name)
    col.add(
        documents=[content],
        metadatas=[meta],
        ids=[f"{slug(title)}_{int(time.time()*1000)}"]
    )
    return True

def import_directory(dir_path, collection_name, agent_name='Semantic Memory'):
    """递归导入目录下所有 .md 文件"""
    if not os.path.isdir(dir_path):
        print(f"❌ 目录不存在：{dir_path}")
        return

    md_files = []
    for root, _, files in os.walk(dir_path):
        # 跳过缓存目录
        if 'tfidf_cache' in root or 'bm25_cache' in root or '__pycache__' in root:
            continue
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))

    if not md_files:
        print(f"⚠️  目录下没有 .md 文件：{dir_path}")
        return

    print(f"\n📁 开始导入：{dir_path}")
    print(f"   → Collection: {collection_name}")
    print(f"   → Agent: {agent_name}")
    print(f"   → 文件数：{len(md_files)}\n")

    success = 0
    for fp in sorted(md_files):
        if import_file(fp, collection_name, agent_name):
            print(f"  ✅ {os.path.basename(fp)}")
            success += 1
        time.sleep(0.05)  # 避免请求过快

    col = ensure_collection(collection_name)
    print(f"\n📊 导入完成：{success}/{len(md_files)} 个文件")
    print(f"   Collection '{collection_name}' 共 {col.count()} 条记录")

# ── CLI ──────────────────────────────────────────────────────────
if __name__ == '__main__':
    # 默认：导入 workspace/memory 目录到 memories collection
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # skill根目录的父目录
    dir_path  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(workspace, 'memory')
    coll_name = sys.argv[2] if len(sys.argv) > 2 else 'memories'
    agent     = sys.argv[3] if len(sys.argv) > 3 else '百晓生'

    import_directory(dir_path, coll_name, agent)
