#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
向量化现有内容 - 阿里云 Embedding-v3
"""

import os
import glob
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path

import dashscope
from dashscope import TextEmbedding
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from chromadb.config import Settings

# 配置
WORKSPACE = r"C:\Users\Xiabi\.openclaw\workspace"
CHROMA_DB_PATH = os.path.join(WORKSPACE, "chroma_db")
API_KEY = "sk-1f3847debc3e492e81f64115b20c6d82"

dashscope.api_key = API_KEY

# 文本分块
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    length_function=len,
    separators=["\n\n", "\n", "。", "!", "?", " ", ""]
)

def read_file(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败 {filepath}: {e}")
        return None

def get_embeddings(texts):
    """批量获取文本向量"""
    try:
        response = TextEmbedding.call(
            model='text-embedding-v3',
            input=texts
        )
        
        # 检查响应格式
        if isinstance(response, dict):
            if 'output' in response and 'embeddings' in response['output']:
                return response['output']['embeddings']
        else:
            if hasattr(response, 'output') and hasattr(response.output, 'embeddings'):
                return response.output.embeddings
        
        print(f"响应格式异常：{response}")
        return None
    except Exception as e:
        print(f"获取向量异常：{e}")
        return None

def generate_id(text, source, index):
    """为文本生成唯一 ID"""
    unique_str = f"{source}:{index}:{text[:50]}"
    return hashlib.md5(unique_str.encode('utf-8')).hexdigest()

def main():
    print("=" * 60)
    print("Starting vectorization...")
    print("=" * 60)
    
    # 1. 收集所有文件
    files_to_vectorize = []
    
    # USER.md
    user_md = os.path.join(WORKSPACE, "USER.md")
    if os.path.exists(user_md):
        files_to_vectorize.append(user_md)
    
    # MEMORY.md
    memory_md = os.path.join(WORKSPACE, "MEMORY.md")
    if os.path.exists(memory_md):
        files_to_vectorize.append(memory_md)
    
    # memory/*.md
    memory_files = glob.glob(os.path.join(WORKSPACE, "memory", "*.md"))
    files_to_vectorize.extend(memory_files)
    
    # best_practices.jsonl
    bp_file = os.path.join(WORKSPACE, "best_practices.jsonl")
    if os.path.exists(bp_file):
        files_to_vectorize.append(bp_file)
    
    # knowledge/**/*.md
    knowledge_files = glob.glob(os.path.join(WORKSPACE, "knowledge", "**", "*.md"), recursive=True)
    files_to_vectorize.extend(knowledge_files)
    
    print(f"\nFound {len(files_to_vectorize)} files")
    
    # 2. 读取并分块
    all_documents = []
    stats = {
        'files': {},
        'total_chunks': 0
    }
    
    for filepath in files_to_vectorize:
        content = read_file(filepath)
        if content:
            rel_path = os.path.relpath(filepath, WORKSPACE)
            
            # 对于 jsonl 文件，逐行处理
            if filepath.endswith('.jsonl'):
                lines = content.strip().split('\n')
                chunk_count = 0
                for i, line in enumerate(lines):
                    try:
                        data = json.loads(line)
                        text = json.dumps(data, ensure_ascii=False)
                        chunks = splitter.split_text(text)
                        for chunk in chunks:
                            all_documents.append(Document(
                                page_content=chunk,
                                metadata={
                                    'source': rel_path,
                                    'line': i + 1,
                                    'type': 'jsonl'
                                }
                            ))
                            chunk_count += 1
                    except Exception as e:
                        print(f"  Parse JSONL line {i+1} failed: {e}")
                
                stats['files'][rel_path] = chunk_count
                stats['total_chunks'] += chunk_count
            else:
                # 普通文本文件
                chunks = splitter.split_text(content)
                for chunk in chunks:
                    all_documents.append(Document(
                        page_content=chunk,
                        metadata={
                            'source': rel_path,
                            'type': 'markdown'
                        }
                    ))
                stats['files'][rel_path] = len(chunks)
                stats['total_chunks'] += len(chunks)
    
    print(f"Chunking complete: {stats['total_chunks']} chunks")
    
    # 3. 批量生成向量
    print("\nGenerating embeddings...")
    
    # 分批处理，每批 10 个文本块
    batch_size = 10
    all_embeddings = []
    all_texts = []
    all_metadatas = []
    all_ids = []
    
    for i in range(0, len(all_documents), batch_size):
        batch_docs = all_documents[i:i+batch_size]
        batch_texts = [doc.page_content for doc in batch_docs]
        
        emb_results = get_embeddings(batch_texts)
        
        if emb_results:
            for emb_data in emb_results:
                idx = emb_data['text_index']
                doc_idx = i + idx
                all_embeddings.append(emb_data['embedding'])
                all_texts.append(batch_texts[idx])
                all_metadatas.append(batch_docs[idx].metadata)
                all_ids.append(generate_id(batch_texts[idx], batch_docs[idx].metadata['source'], doc_idx))
            
            progress = min(i + batch_size, len(all_documents))
            print(f"  Progress: {progress}/{len(all_documents)} ({progress/len(all_documents)*100:.1f}%)")
        else:
            print(f"  Batch failed")
        
        # 避免频率限制
        time.sleep(0.5)
    
    print(f"\nEmbeddings generated: {len(all_embeddings)} vectors")
    
    # 4. 存入 ChromaDB
    print("\nStoring to ChromaDB...")
    
    # 删除旧数据库（避免重复）
    if os.path.exists(CHROMA_DB_PATH):
        import shutil
        shutil.rmtree(CHROMA_DB_PATH)
        print("  Cleaned old database")
    
    # 创建新数据库（不指定 embedding_function，使用自定义 ID）
    from chromadb import PersistentClient
    client = PersistentClient(path=CHROMA_DB_PATH)
    
    # 创建 collection，指定维度为 1024
    collection = client.create_collection(
        name='user_preferences',
        metadata={"hnsw:space": "cosine"}
    )
    
    # 批量添加（Chroma 限制每次最多 5461 条）
    batch_size_chroma = 100
    for i in range(0, len(all_texts), batch_size_chroma):
        end_idx = min(i + batch_size_chroma, len(all_texts))
        collection.add(
            ids=all_ids[i:end_idx],
            embeddings=all_embeddings[i:end_idx],
            documents=all_texts[i:end_idx],
            metadatas=all_metadatas[i:end_idx]
        )
        print(f"  Added {end_idx}/{len(all_texts)} documents")
    
    print("  ChromaDB storage complete")
    
    # 5. 保存统计信息
    stats_output = {
        'timestamp': datetime.now().isoformat(),
        'total_files': len(files_to_vectorize),
        'total_chunks': stats['total_chunks'],
        'total_vectors': len(all_embeddings),
        'files_breakdown': stats['files'],
        'chroma_db_path': CHROMA_DB_PATH,
        'embedding_dimension': 1024
    }
    
    stats_file = os.path.join(WORKSPACE, "vectorization_stats.json")
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats_output, f, ensure_ascii=False, indent=2)
    
    print(f"\nStats saved to: {stats_file}")
    print("\n" + "=" * 60)
    print("Vectorization complete!")
    print("=" * 60)
    
    # 打印详细统计
    print("\nVectorization Statistics:")
    print(f"  Total files: {len(files_to_vectorize)}")
    print(f"  Total chunks: {stats['total_chunks']}")
    print(f"  Total vectors: {len(all_embeddings)}")
    print(f"  Embedding dimension: 1024")
    print(f"\n  File breakdown:")
    for filepath, chunk_count in sorted(stats['files'].items()):
        print(f"    - {filepath}: {chunk_count} chunks")
    
    return stats_output

if __name__ == "__main__":
    main()
