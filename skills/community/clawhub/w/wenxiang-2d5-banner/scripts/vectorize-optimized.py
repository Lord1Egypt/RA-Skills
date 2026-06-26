#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化的向量化脚本
- 批量处理（10 个/批）
- 增量更新（只处理新增/修改）
- 文件哈希检测
- 多线程并行处理
"""

import hashlib
import json
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import dashscope
from dashscope import TextEmbedding
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# 配置
DASHSCOPE_API_KEY = "sk-1f3847debc3e492e81f64115b20c6d82"
CHROMA_PERSIST_DIR = "C:/Users/Xiabi/.openclaw/workspace/chroma_db"
WORKSPACE_DIR = "C:/Users/Xiabi/.openclaw/workspace"
HASH_LOG_FILE = "C:/Users/Xiabi/.openclaw/workspace/vectorize_hashes.json"
BATCH_SIZE = 10  # 每批 10 个文本
MAX_WORKERS = 5  # 5 个线程并行

dashscope.api_key = DASHSCOPE_API_KEY

def get_file_hash(file_path):
    """获取文件哈希值"""
    try:
        content = Path(file_path).read_text(encoding='utf-8')
        return hashlib.md5(content.encode()).hexdigest()
    except Exception as e:
        print(f"⚠️  {file_path} 读取失败：{e}")
        return None

def load_file_hashes():
    """加载文件哈希日志"""
    if Path(HASH_LOG_FILE).exists():
        with open(HASH_LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_file_hashes(hashes):
    """保存文件哈希日志"""
    Path(HASH_LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(HASH_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(hashes, f, ensure_ascii=False, indent=2, default=str)

def vectorize_batch(texts):
    """批量向量化"""
    try:
        response = TextEmbedding.call(model='text-embedding-v3', input=texts)
        if response.status_code == 200:
            return [item['embedding'] for item in response.output['embeddings']]
        else:
            print(f"❌ API 错误：{response.code} - {response.message}")
            return None
    except Exception as e:
        print(f"❌ 向量化失败：{e}")
        return None

def main():
    print("=" * 60)
    print("🚀 优化的向量化脚本")
    print("=" * 60)
    print()
    
    # 1. 加载文件哈希
    print("📊 加载文件哈希...")
    file_hashes = load_file_hashes()
    print(f"   已记录：{len(file_hashes)} 个文件")
    print()
    
    # 2. 扫描文件
    print("📂 扫描文件...")
    files_to_vectorize = [
        ("USER.md", "user_preference"),
        ("MEMORY.md", "longterm_memory"),
        ("best_practices.jsonl", "best_practice"),
    ]
    
    # 添加 memory/*.md 文件
    memory_dir = Path(WORKSPACE_DIR) / "memory"
    if memory_dir.exists():
        for md_file in memory_dir.glob("*.md"):
            files_to_vectorize.append((f"memory/{md_file.name}", "daily_memory"))
    
    # 添加 knowledge/**/*.md 文件
    knowledge_dir = Path(WORKSPACE_DIR) / "knowledge"
    if knowledge_dir.exists():
        for md_file in knowledge_dir.rglob("*.md"):
            files_to_vectorize.append((f"knowledge/{md_file.relative_to(knowledge_dir).as_posix()}", "knowledge"))
    
    print(f"   待扫描：{len(files_to_vectorize)} 个文件")
    print()
    
    # 3. 检测变更
    print("🔍 检测变更...")
    new_or_modified = []
    documents = []
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    for file_path, doc_type in files_to_vectorize:
        full_path = Path(WORKSPACE_DIR) / file_path
        if not full_path.exists():
            print(f"⚠️  文件不存在：{file_path}")
            continue
        
        current_hash = get_file_hash(full_path)
        if not current_hash:
            continue
        
        if file_hashes.get(file_path) != current_hash:
            print(f"✅ 变更：{file_path}")
            new_or_modified.append(file_path)
            file_hashes[file_path] = current_hash
            
            # 读取并分块
            try:
                content = full_path.read_text(encoding='utf-8')
                chunks = splitter.split_text(content)
                
                for i, chunk in enumerate(chunks):
                    documents.append(Document(
                        page_content=chunk,
                        metadata={
                            "source": file_path,
                            "type": doc_type,
                            "chunk": i
                        }
                    ))
            except Exception as e:
                print(f"❌ {file_path} 分块失败：{e}")
        else:
            print(f"⏭️  跳过：{file_path}")
    
    print()
    print(f"📊 变更统计：{len(new_or_modified)} 个文件，{len(documents)} 个文本块")
    print()
    
    # 4. 批量向量化
    if not documents:
        print("✅ 无变更，跳过向量化")
        return
    
    print("🧠 批量向量化...")
    all_texts = [doc.page_content for doc in documents]
    all_embeddings = []
    
    # 分批处理
    batches = [all_texts[i:i+BATCH_SIZE] for i in range(0, len(all_texts), BATCH_SIZE)]
    print(f"   共 {len(batches)} 批，每批 {BATCH_SIZE} 个文本")
    
    # 多线程并行处理
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(executor.map(vectorize_batch, batches))
        
        for i, embeddings in enumerate(results):
            if embeddings:
                all_embeddings.extend(embeddings)
                print(f"   ✅ 批次 {i+1}/{len(batches)}: {len(embeddings)} 个向量")
            else:
                print(f"   ❌ 批次 {i+1}/{len(batches)}: 失败")
    
    print()
    print(f"✅ 向量化完成：{len(all_embeddings)} 个向量")
    print()
    
    # 5. 存入 ChromaDB
    print("💾 存入 ChromaDB...")
    
    # 删除旧集合（避免维度不匹配）
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    try:
        client.delete_collection("user_preferences")
        print("  ✅ 已删除旧集合")
    except:
        print("  ℹ️  旧集合不存在")
    
    # 创建新集合并添加数据
    db = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        collection_name="user_preferences"
    )
    
    db.add_documents(documents=documents, embeddings=all_embeddings)
    
    print(f"  ✅ 已存入 {len(all_embeddings)} 个向量")
    print(f"  ✅ 向量维度：{len(all_embeddings[0])}")
    print()
    
    # 6. 保存哈希日志
    print("💾 保存哈希日志...")
    save_file_hashes(file_hashes)
    print(f"  ✅ 已保存到：{HASH_LOG_FILE}")
    print()
    
    # 7. 测试搜索
    print("🧪 测试语义搜索...")
    test_queries = ["瀑布", "TTS", "供应商", "表情图片", "向量数据库"]
    
    for query in test_queries:
        try:
            # 生成查询向量
            query_response = TextEmbedding.call(model='text-embedding-v3', input=query)
            query_embedding = query_response.output["embeddings"][0]["embedding"]
            
            # 搜索
            results = db.similarity_search_by_vector(query_embedding, k=2)
            
            print(f"\n  查询：'{query}'")
            for i, doc in enumerate(results, 1):
                source = doc.metadata.get("source", "Unknown")
                preview = doc.page_content[:80].replace("\n", " ")
                print(f"    {i}. [{source}] {preview}...")
        except Exception as e:
            print(f"  ❌ '{query}' 搜索失败：{e}")
    
    print()
    print("=" * 60)
    print("🎉 向量化完成！")
    print("=" * 60)
    print()
    print("📊 统计信息：")
    print(f"  - 变更文件：{len(new_or_modified)} 个")
    print(f"  - 文本块数：{len(documents)} 个")
    print(f"  - 向量数量：{len(all_embeddings)} 个")
    print(f"  - 向量维度：{len(all_embeddings[0])}")
    print(f"  - 批次数量：{len(batches)} 批")
    print(f"  - 总耗时：{(datetime.now() - datetime.now()).total_seconds()} 秒")
    print()

if __name__ == "__main__":
    main()
