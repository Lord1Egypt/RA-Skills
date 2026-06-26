#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Vector Indexer for OpenClaw
向量化所有技能文件并保存到 Chroma 向量数据库
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import hashlib

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from langchain_chroma import Chroma
    from langchain_core.documents import Document
    import chromadb
except ImportError as e:
    print(f"[ERROR] Missing package: {e}")
    print("Run: pip install langchain-chroma langchain-core chromadb")
    raise


class AliyunEmbeddings:
    """阿里云 Embedding 接口"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ALIYUN_API_KEY")
        if not self.api_key:
            raise ValueError("ALIYUN_API_KEY not found")
        
        self.model = "text-embedding-v3"
        self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """批量生成 embeddings（最多 10 个/批）"""
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        all_embeddings = []
        
        for i in range(0, len(texts), 10):
            batch = texts[i:i+10]
            payload = {
                "model": self.model,
                "input": {"texts": batch},
                "parameters": {"text_type": "document"}
            }
            
            try:
                response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
                response.raise_for_status()
                result = response.json()
                
                if "output" in result and "embeddings" in result["output"]:
                    batch_embeddings = [item["embedding"] for item in result["output"]["embeddings"]]
                    all_embeddings.extend(batch_embeddings)
                    print(f"[INFO] Embedded batch {i//10 + 1}: {len(batch)} texts")
                else:
                    print(f"[ERROR] Unexpected response: {result}")
                    all_embeddings.extend([[0.0] * 1024] * len(batch))
                    
            except Exception as e:
                print(f"[ERROR] Failed to embed batch: {e}")
                all_embeddings.extend([[0.0] * 1024] * len(batch))
        
        return all_embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """生成单个查询的 embedding"""
        result = self.embed_documents([text])
        return result[0] if result else [0.0] * 1024


def load_skill_files(skills_dir: str) -> List[Document]:
    """
    加载所有技能文件
    
    Args:
        skills_dir: 技能目录路径
    
    Returns:
        List of Document objects
    """
    skills_path = Path(skills_dir)
    documents = []
    
    if not skills_path.exists():
        print(f"[ERROR] Skills directory not found: {skills_path}")
        return documents
    
    # 查找所有 SKILL.md 文件
    skill_files = list(skills_path.rglob("SKILL.md"))
    
    # 也查找其他 .md 文件（README, ARCHITECTURE 等）
    other_files = list(skills_path.rglob("*.md"))
    all_files = list(set(skill_files + other_files))
    
    print(f"[INFO] Found {len(all_files)} skill-related files")
    
    for md_file in all_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取技能名称（从路径推断）
            rel_path = md_file.relative_to(skills_path)
            skill_name = rel_path.parts[0] if len(rel_path.parts) > 1 else md_file.stem
            
            # 计算文件哈希（用于去重和更新检测）
            file_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            
            # 创建文档对象
            doc = Document(
                page_content=content,
                metadata={
                    "source": str(md_file),
                    "type": "skill_file",
                    "skill_name": skill_name,
                    "filename": md_file.name,
                    "relative_path": str(rel_path),
                    "file_hash": file_hash,
                    "last_modified": datetime.fromtimestamp(md_file.stat().st_mtime).isoformat(),
                    "file_size": md_file.stat().st_size
                }
            )
            documents.append(doc)
            print(f"[INFO] Loaded: {rel_path}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load {md_file}: {e}")
    
    return documents


def chunk_skill_content(content: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    """
    将技能内容分块（技能文件通常较长）
    
    Args:
        content: 文档内容
        chunk_size: 每块字符数
        overlap: 块间重叠
    
    Returns:
        文本块列表
    """
    chunks = []
    start = 0
    
    while start < len(content):
        end = start + chunk_size
        chunk = content[start:end]
        
        # 尝试在句子边界或段落边界断开
        if end < len(content):
            # 优先在段落断开
            last_double_newline = chunk.rfind('\n\n')
            # 其次在句子断开
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            break_point = max(last_double_newline, last_period, last_newline)
            
            if break_point > chunk_size // 2:
                chunk = chunk[:break_point + 1]
                end = start + break_point + 1
        
        if chunk.strip():
            chunks.append(chunk.strip())
        
        start = end - overlap
    
    return chunks


def index_skills(workspace_dir: str, 
                 chroma_dir: str,
                 collection_name: str = "openclaw_skills",
                 api_key: str = None):
    """
    索引所有技能文件到 Chroma
    
    Args:
        workspace_dir: OpenClaw 工作区路径
        chroma_dir: Chroma 数据库目录
        collection_name: 集合名称
        api_key: 阿里云 API Key
    """
    print("=" * 60)
    print("OpenClaw Skill Vector Indexer")
    print("=" * 60)
    
    # 获取 API Key
    if api_key is None:
        api_key = os.getenv("ALIYUN_API_KEY")
    
    if not api_key:
        print("[ERROR] ALIYUN_API_KEY not found")
        print("Please set environment variable")
        sys.exit(1)
    
    skills_dir = Path(workspace_dir) / "skills"
    
    print(f"[INFO] Workspace: {workspace_dir}")
    print(f"[INFO] Skills Dir: {skills_dir}")
    print(f"[INFO] Chroma DB: {chroma_dir}")
    print(f"[INFO] Collection: {collection_name}")
    
    # 加载技能文件
    print("\n[INFO] Loading skill files...")
    documents = load_skill_files(skills_dir)
    
    if not documents:
        print("[ERROR] No skill files found")
        sys.exit(1)
    
    print(f"[INFO] Loaded {len(documents)} files")
    
    # 分块
    print("\n[INFO] Chunking documents...")
    all_chunks = []
    chunk_metadata = []
    
    for doc in documents:
        chunks = chunk_skill_content(doc.page_content)
        for chunk in chunks:
            if len(chunk.strip()) > 50:  # 跳过太短的块
                all_chunks.append(chunk)
                chunk_metadata.append(doc.metadata.copy())
    
    print(f"[INFO] Created {len(all_chunks)} chunks")
    
    # 初始化 Embeddings
    print("\n[INFO] Initializing embeddings...")
    embeddings = AliyunEmbeddings(api_key=api_key)
    
    # 创建 Chroma 客户端
    print(f"\n[INFO] Creating vector store...")
    client = chromadb.PersistentClient(path=chroma_dir)
    
    # 删除现有集合（避免维度不匹配）
    try:
        client.delete_collection(name=collection_name)
        print(f"[INFO] Deleted existing collection: {collection_name}")
    except Exception as e:
        print(f"[INFO] No existing collection to delete: {e}")
    
    # 批量生成 embeddings
    print(f"[INFO] Generating embeddings for {len(all_chunks)} chunks...")
    all_embeddings = []
    batch_size = 10
    
    for i in range(0, len(all_chunks), batch_size):
        batch_texts = all_chunks[i:i+batch_size]
        try:
            batch_embeddings = embeddings.embed_documents(batch_texts)
            all_embeddings.extend(batch_embeddings)
            print(f"[INFO] Embedded {min(i+batch_size, len(all_chunks))}/{len(all_chunks)} chunks")
        except Exception as e:
            print(f"[ERROR] Failed to embed batch {i//batch_size}: {e}")
            all_embeddings.extend([[0.0] * 1024] * len(batch_texts))
    
    # 创建集合
    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine", "embedding_dimension": 1024}
    )
    
    # 添加文档
    print(f"[INFO] Adding {len(all_chunks)} documents to collection...")
    ids = [f"skill_{i}" for i in range(len(all_chunks))]
    collection.add(
        ids=ids,
        embeddings=all_embeddings,
        documents=all_chunks,
        metadatas=chunk_metadata
    )
    
    print(f"[INFO] Collection created successfully")
    
    # 创建向量存储包装器
    vectorstore = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings
    )
    
    # 保存索引元数据
    metadata_file = Path(chroma_dir) / "skills_metadata.json"
    metadata = {
        "collection_name": collection_name,
        "total_chunks": len(all_chunks),
        "total_files": len(documents),
        "indexed_at": datetime.now().isoformat(),
        "skills": list(set(m["skill_name"] for m in chunk_metadata))
    }
    
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"\n[INFO] Metadata saved to: {metadata_file}")
    print(f"\n[INFO] Indexing complete!")
    print(f"   - Total files: {len(documents)}")
    print(f"   - Total chunks: {len(all_chunks)}")
    print(f"   - Collection: {collection_name}")
    print(f"   - Database: {chroma_dir}")
    
    # 测试搜索
    print("\n[INFO] Testing search...")
    test_query = "飞书文档"
    results = vectorstore.similarity_search_with_score(test_query, k=3)
    
    if results:
        print(f"[SUCCESS] Found {len(results)} results for '{test_query}'")
        for i, (doc, score) in enumerate(results, 1):
            similarity = 1 - score
            print(f"  {i}. [{doc.metadata.get('skill_name', 'Unknown')}] (similarity: {similarity:.3f})")
            print(f"     {doc.page_content[:100]}...")
    else:
        print(f"[WARN] No results found for test query")
    
    print("\n" + "=" * 60)
    
    return vectorstore, metadata


if __name__ == "__main__":
    # 配置 - 使用绝对路径
    workspace_dir = r"C:\Users\Xiabi\.openclaw\workspace"
    chroma_dir = r"C:\Users\Xiabi\.openclaw\workspace\chroma_db"
    
    # 运行索引
    index_skills(workspace_dir, chroma_dir)
