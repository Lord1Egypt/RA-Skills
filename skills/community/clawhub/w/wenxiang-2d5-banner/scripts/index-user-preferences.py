#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Index User Preferences to Vector Database
向量化用户偏好：MEMORY.md, USER.md, memory/*.md
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Import dependencies
try:
    from langchain_chroma import Chroma
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document
    import dashscope
    from dashscope import TextEmbedding
except ImportError as e:
    print(f"[ERROR] Missing package: {e}")
    print("Run: pip install langchain langchain-chroma dashscope langchain-text-splitters")
    sys.exit(1)


class AliyunEmbeddings:
    """阿里云 Embedding 封装"""
    
    def __init__(self, api_key: str, model: str = "text-embedding-v3"):
        dashscope.api_key = api_key
        self.model = model
    
    def embed_documents(self, texts: list) -> list:
        """批量生成向量（每次最多 10 个）"""
        all_embeddings = []
        batch_size = 10
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            try:
                response = TextEmbedding.call(
                    model=self.model,
                    input=batch
                )
                if response.status_code == 200:
                    embeddings = [item["embedding"] for item in response.output["embeddings"]]
                    all_embeddings.extend(embeddings)
                    print(f"  Progress: {min(i+batch_size, len(texts))}/{len(texts)}")
                else:
                    print(f"[WARN] API Error: {response.code} - {response.message}")
            except Exception as e:
                print(f"[WARN] Embedding Error: {e}")
        
        return all_embeddings


def load_user_preference_files(workspace: str) -> list:
    """读取用户偏好相关文件"""
    documents = []
    
    print(f"[INFO] Scanning workspace: {workspace}")
    
    # 1. 读取 USER.md
    user_md = Path(workspace) / "USER.md"
    if user_md.exists():
        try:
            content = user_md.read_text(encoding="utf-8")
            documents.append(Document(
                page_content=content,
                metadata={
                    "source": "USER.md",
                    "type": "user_preference",
                    "loaded_at": datetime.now().isoformat()
                }
            ))
            print(f"[OK] USER.md ({len(content)} chars)")
        except Exception as e:
            print(f"[WARN] Failed to read USER.md: {e}")
    
    # 2. 读取 MEMORY.md
    memory_md = Path(workspace) / "MEMORY.md"
    if memory_md.exists():
        try:
            content = memory_md.read_text(encoding="utf-8")
            documents.append(Document(
                page_content=content,
                metadata={
                    "source": "MEMORY.md",
                    "type": "longterm_memory",
                    "loaded_at": datetime.now().isoformat()
                }
            ))
            print(f"[OK] MEMORY.md ({len(content)} chars)")
        except Exception as e:
            print(f"[WARN] Failed to read MEMORY.md: {e}")
    
    # 3. 读取 memory/*.md (每日记忆)
    memory_dir = Path(workspace) / "memory"
    if memory_dir.exists():
        md_files = list(memory_dir.glob("*.md"))
        print(f"[INFO] Found {len(md_files)} daily memory files")
        
        for file in md_files:
            try:
                content = file.read_text(encoding="utf-8")
                if len(content.strip()) > 0:
                    documents.append(Document(
                        page_content=content,
                        metadata={
                            "source": f"memory/{file.name}",
                            "type": "daily_memory",
                            "date": file.stem,
                            "loaded_at": datetime.now().isoformat()
                        }
                    ))
            except Exception as e:
                print(f"[WARN] Failed to read {file.name}: {e}")
    
    # 4. 读取 memory/self-improving/best_practices.jsonl
    best_practices = Path(workspace) / "memory" / "self-improving" / "best_practices.jsonl"
    if best_practices.exists():
        try:
            content = best_practices.read_text(encoding="utf-8")
            documents.append(Document(
                page_content=content,
                metadata={
                    "source": "memory/self-improving/best_practices.jsonl",
                    "type": "best_practice",
                    "loaded_at": datetime.now().isoformat()
                }
            ))
            print(f"[OK] best_practices.jsonl ({len(content)} chars)")
        except Exception as e:
            print(f"[WARN] Failed to read best_practices.jsonl: {e}")
    
    return documents


def split_documents(documents: list, chunk_size: int = 512, chunk_overlap: int = 50) -> list:
    """文本分块"""
    print(f"\n[INFO] Splitting text (chunk_size={chunk_size}, overlap={chunk_overlap})")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = splitter.split_documents(documents)
    print(f"[OK] {len(documents)} docs -> {len(chunks)} chunks")
    
    return chunks


def create_vectorstore(chunks: list, embeddings, persist_dir: str, collection_name: str = "user_preferences"):
    """创建向量数据库"""
    print(f"\n[INFO] Creating vector database: {persist_dir}")
    
    # Delete existing collection to avoid dimension mismatch
    import chromadb
    client = chromadb.PersistentClient(path=persist_dir)
    try:
        client.delete_collection(collection_name)
        print(f"[INFO] Deleted existing collection: {collection_name}")
    except:
        pass
    
    # Create vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name=collection_name
    )
    
    print(f"[OK] Vector database created!")
    print(f"   - Location: {persist_dir}")
    print(f"   - Collection: {collection_name}")
    print(f"   - Documents: {len(chunks)}")
    
    return vectorstore


def test_search(vectorstore, test_queries: list):
    """测试搜索"""
    print(f"\n[TEST] Vector search test...")
    
    for query in test_queries:
        print(f"\n  Query: '{query}'")
        results = vectorstore.similarity_search(query, k=3)
        
        if results:
            print(f"  [OK] Found {len(results)} results:")
            for i, doc in enumerate(results, 1):
                source = doc.metadata.get("source", "Unknown")
                preview = doc.page_content[:100].replace("\n", " ")
                print(f"    {i}. [{source}] {preview}...")
        else:
            print(f"  [WARN] No results found")


def main():
    """主函数"""
    print("=" * 70)
    print("User Preferences Vectorization")
    print("=" * 70)
    print()
    
    # Configuration
    workspace = os.getenv("OPENCLAW_WORKSPACE", r"C:\Users\Xiabi\.openclaw\workspace")
    api_key = os.getenv("ALIYUN_API_KEY")
    chroma_dir = os.getenv("CHROMA_PERSIST_DIR", os.path.join(workspace, "chroma_db"))
    chunk_size = int(os.getenv("CHUNK_SIZE", "512"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "50"))
    
    # Check API Key
    if not api_key:
        print("[ERROR] Missing ALIYUN_API_KEY environment variable")
        print("Set: $env:ALIYUN_API_KEY='sk-xxx'")
        return 1
    
    print(f"[CONFIG]")
    print(f"   - Workspace: {workspace}")
    print(f"   - Chroma DB: {chroma_dir}")
    print(f"   - Chunk Size: {chunk_size}")
    print()
    
    # 1. Load files
    print("[1/4] Loading user preference files...")
    documents = load_user_preference_files(workspace)
    if not documents:
        print("[ERROR] No files found")
        return 1
    print(f"[OK] Loaded {len(documents)} documents")
    
    # 2. Split text
    print("\n[2/4] Splitting text...")
    chunks = split_documents(documents, chunk_size, chunk_overlap)
    
    # 3. Generate embeddings
    print("\n[3/4] Generating embeddings (calling Aliyun API)...")
    embeddings = AliyunEmbeddings(api_key=api_key)
    
    # 4. Create vector store
    print("\n[4/4] Creating vector database...")
    vectorstore = create_vectorstore(chunks, embeddings, chroma_dir)
    
    # Test search
    test_queries = [
        "视觉学习者 Mermaid 图表",
        "表情图片发送顺序",
        "供应商直连系统",
    ]
    test_search(vectorstore, test_queries)
    
    print("\n" + "=" * 70)
    print("Vectorization Complete!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
