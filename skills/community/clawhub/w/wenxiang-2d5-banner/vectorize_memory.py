#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量化脚本 - 将 MEMORY.md 和 memory/*.md 文件向量化并存储到 Chroma 数据库
使用阿里云 text-embedding-v2 模型
"""

import os
import sys
import hashlib
import json
from pathlib import Path
from datetime import datetime
import time

# 添加必要的库
try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    print("正在安装 chromadb...")
    os.system("pip install chromadb -q")
    import chromadb
    from chromadb.config import Settings

try:
    import requests
except ImportError:
    print("正在安装 requests...")
    os.system("pip install requests -q")
    import requests

# 配置
WORKSPACE = Path(r"C:\Users\Xiabi\.openclaw\workspace")
MEMORY_DIR = WORKSPACE / "memory"
CHROMA_DB_PATH = WORKSPACE / "chroma_db"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
ALIYUN_API_KEY = os.environ.get("ALIYUN_API_KEY", "sk-1f3847debc3e492e81f64115b20c6d82")
ALIYUN_EMBEDDING_URL = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"

# 阿里云 text-embedding-v2 配置
ALIYUN_MODEL = "text-embedding-v2"

class MemoryVectorizer:
    def __init__(self):
        self.api_key = ALIYUN_API_KEY
        self.client = None
        self.collection = None
        self.stats = {
            "files_processed": 0,
            "chunks_created": 0,
            "vectors_stored": 0,
            "errors": []
        }
        
    def get_embedding(self, text):
        """调用阿里云 text-embedding-v2 API 获取向量"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": ALIYUN_MODEL,
            "input": {
                "texts": [text]
            },
            "parameters": {
                "text_type": "document"
            }
        }
        
        try:
            response = requests.post(ALIYUN_EMBEDDING_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            # 阿里云 API 返回格式：output.embeddings[0].embedding
            if "output" in result and "embeddings" in result["output"]:
                embedding = result["output"]["embeddings"][0]["embedding"]
                return embedding
            elif "data" in result and "embeddings" in result["data"]:
                embedding = result["data"]["embeddings"][0]["embedding"]
                return embedding
            else:
                raise Exception(f"API 返回格式异常：{str(result)[:200]}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"阿里云 API 调用失败：{str(e)}")
    
    def chunk_text(self, text, chunk_size=500, overlap=50):
        """将文本分块，保留语义完整性"""
        chunks = []
        
        # 按段落分割
        paragraphs = text.split('\n\n')
        current_chunk = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # 如果块太大，进一步分割
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > chunk_size * 1.5:
                # 按句子分割
                sentences = chunk.replace('\n', ' ').split('。')
                sub_chunk = ""
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    if len(sub_chunk) + len(sentence) < chunk_size:
                        sub_chunk += sentence + "。"
                    else:
                        if sub_chunk:
                            final_chunks.append(sub_chunk.strip())
                        sub_chunk = sentence + "。"
                if sub_chunk.strip():
                    final_chunks.append(sub_chunk.strip())
            else:
                final_chunks.append(chunk)
        
        return final_chunks
    
    def initialize_chroma(self):
        """初始化 Chroma 数据库"""
        print(f"正在初始化 Chroma 数据库：{CHROMA_DB_PATH}")
        
        # 创建持久化客户端
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DB_PATH),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # 创建或获取集合
        try:
            self.collection = self.client.get_collection("memory_vectors")
            print("[OK] 已加载现有集合 'memory_vectors'")
        except Exception:
            self.collection = self.client.create_collection("memory_vectors")
            print("[OK] 已创建新集合 'memory_vectors'")
    
    def process_file(self, file_path):
        """处理单个文件并向量化"""
        print(f"\n处理文件：{file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            error_msg = f"读取文件失败 {file_path.name}: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self.stats["errors"].append(error_msg)
            return
        
        # 分块
        chunks = self.chunk_text(content)
        print(f"  分割为 {len(chunks)} 个块")
        
        # 向量化并存储
        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
            
            # 生成唯一 ID
            chunk_id = hashlib.md5(
                f"{file_path.name}:{i}:{chunk[:100]}".encode('utf-8')
            ).hexdigest()
            
            # 获取向量
            try:
                embedding = self.get_embedding(chunk)
            except Exception as e:
                error_msg = f"向量化失败 {file_path.name}#{i}: {str(e)}"
                print(f"  [ERROR] {error_msg}")
                self.stats["errors"].append(error_msg)
                continue
            
            # 元数据
            metadata = {
                "source_file": file_path.name,
                "chunk_index": i,
                "chunk_size": len(chunk),
                "created_at": datetime.now().isoformat(),
                "content_preview": chunk[:200]
            }
            
            # 存储到 Chroma
            try:
                self.collection.upsert(
                    ids=[chunk_id],
                    embeddings=[embedding],
                    metadatas=[metadata],
                    documents=[chunk]
                )
                self.stats["vectors_stored"] += 1
            except Exception as e:
                error_msg = f"存储向量失败 {file_path.name}#{i}: {str(e)}"
                print(f"  [ERROR] {error_msg}")
                self.stats["errors"].append(error_msg)
                continue
            
            if (i + 1) % 10 == 0:
                print(f"  已处理 {i + 1}/{len(chunks)} 个块")
            
            # 避免 API 限流
            time.sleep(0.1)
        
        self.stats["files_processed"] += 1
        self.stats["chunks_created"] += len(chunks)
        print(f"  [OK] 完成：{len(chunks)} 个块，{len(chunks)} 个向量")
    
    def search(self, query, top_k=5):
        """搜索相似内容"""
        print(f"\n搜索测试：'{query}'")
        
        try:
            query_embedding = self.get_embedding(query)
        except Exception as e:
            print(f"[ERROR] 搜索失败：{str(e)}")
            return []
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        if results and results['documents'] and results['documents'][0]:
            print(f"  找到 {len(results['documents'][0])} 个相关结果：")
            for i, (doc, meta, dist) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                print(f"\n  [{i+1}] 来源：{meta['source_file']}")
                print(f"      相似度：{1 - dist:.4f}")
                preview = doc[:200].replace('\n', ' ').replace('\r', '')
                print(f"      内容：{preview}...")
            return results
        else:
            print("  未找到结果")
            return []
    
    def run(self):
        """执行完整向量化流程"""
        print("=" * 60)
        print("[START] 开始向量化流程")
        print("=" * 60)
        print(f"工作目录：{WORKSPACE}")
        print(f"Chroma 路径：{CHROMA_DB_PATH}")
        print(f"API Key: {self.api_key[:10]}...")
        print(f"模型：{ALIYUN_MODEL}")
        
        # 初始化 Chroma
        self.initialize_chroma()
        
        # 收集所有文件
        files_to_process = []
        
        # MEMORY.md
        if MEMORY_FILE.exists():
            files_to_process.append(MEMORY_FILE)
            print(f"\n[OK] 找到 MEMORY.md")
        else:
            print(f"\n[ERROR] MEMORY.md 不存在")
        
        # memory/*.md
        if MEMORY_DIR.exists():
            md_files = list(MEMORY_DIR.glob("*.md"))
            files_to_process.extend(md_files)
            print(f"[OK] 找到 {len(md_files)} 个 memory/*.md 文件")
        else:
            print(f"[ERROR] memory 目录不存在")
        
        print(f"\n总计：{len(files_to_process)} 个文件待处理")
        
        # 处理每个文件
        for file_path in files_to_process:
            self.process_file(file_path)
        
        # 统计结果
        print("\n" + "=" * 60)
        print("[STATS] 向量化结果统计")
        print("=" * 60)
        print(f"处理文件数：{self.stats['files_processed']}")
        print(f"创建块数：{self.stats['chunks_created']}")
        print(f"存储向量数：{self.stats['vectors_stored']}")
        print(f"错误数：{len(self.stats['errors'])}")
        
        if self.stats['errors']:
            print("\n错误详情:")
            for error in self.stats['errors'][:10]:  # 只显示前 10 个错误
                print(f"  - {error}")
        
        # 测试搜索
        print("\n" + "=" * 60)
        print("[TEST] 搜索功能测试")
        print("=" * 60)
        
        test_queries = [
            "Thomas 的偏好是什么？",
            "供应商直连系统进度",
            "技能选择原则"
        ]
        
        for query in test_queries:
            self.search(query, top_k=3)
        
        # 保存统计信息
        stats_file = WORKSPACE / "vectorization_stats.json"
        stats_data = {
            "timestamp": datetime.now().isoformat(),
            "files_processed": self.stats["files_processed"],
            "chunks_created": self.stats["chunks_created"],
            "vectors_stored": self.stats["vectors_stored"],
            "errors_count": len(self.stats["errors"]),
            "errors": self.stats["errors"]
        }
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n[OK] 统计信息已保存到：{stats_file}")
        print("\n" + "=" * 60)
        print("[COMPLETE] 向量化流程完成！")
        print("=" * 60)
        
        return self.stats

if __name__ == "__main__":
    vectorizer = MemoryVectorizer()
    stats = vectorizer.run()
    
    # 退出码
    if stats["errors"]:
        sys.exit(1)
    else:
        sys.exit(0)


