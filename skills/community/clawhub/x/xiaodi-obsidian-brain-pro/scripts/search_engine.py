#!/usr/bin/env python3
"""
Obsidian-Brain-Pro 语义检索引擎 v1.0
使用 Ollama (nomic-embed-text) 进行本地语义搜索
"""

import os
import sys
import json
import requests
from pathlib import Path

# 配置
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://192.168.3.120:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "nomic-embed-text")
OBSIDIAN_PATHS = [
    "~/Obsidian/Daily Notes",
    "~/Obsidian/每日笔记",
    "~/.openclaw/workspace/memory"
]

def get_embedding(text: str) -> list:
    """调用 Ollama 获取文本 embedding"""
    url = f"{OLLAMA_BASE_URL}/api/embeddings"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": text
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json().get("embedding", [])
    except Exception as e:
        print(f"[ERROR] Ollama 请求失败: {e}")
        return []

def cosine_similarity(a: list, b: list) -> float:
    """计算余弦相似度"""
    if len(a) != len(b):
        return 0.0
    
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x ** 2 for x in a) ** 0.5
    norm_b = sum(x ** 2 for x in b) ** 0.5
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)

def search_notes(query: str, top_k: int = 5) -> list:
    """语义搜索笔记"""
    
    # 获取查询 embedding
    query_embedding = get_embedding(query)
    if not query_embedding:
        print("[ERROR] 无法获取查询 embedding")
        return []
    
    # 搜索所有笔记文件
    results = []
    
    for path_str in OBSIDIAN_PATHS:
        path = Path(path_str).expanduser()
        if not path.exists():
            continue
        
        for md_file in path.glob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                
                # 获取文件 embedding
                file_embedding = get_embedding(content[:500])  # 只取前500字符
                
                if file_embedding:
                    similarity = cosine_similarity(query_embedding, file_embedding)
                    
                    results.append({
                        "file": str(md_file),
                        "similarity": similarity,
                        "preview": content[:200] + "..." if len(content) > 200 else content
                    })
            except Exception as e:
                print(f"[WARN] 读取文件失败: {md_file}: {e}")
    
    # 按相似度排序
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    return results[:top_k]

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python search_engine.py <查询内容> [top_k]")
        print("示例: python search_engine.py '最近身体咋样' 5")
        sys.exit(1)
    
    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print(f"[INFO] 查询: {query}")
    print(f"[INFO] Top-K: {top_k}")
    print(f"[INFO] Ollama: {OLLAMA_BASE_URL}/{OLLAMA_MODEL}")
    print()
    
    results = search_notes(query, top_k)
    
    if not results:
        print("[WARN] 无搜索结果")
        sys.exit(0)
    
    print("=== 搜索结果 ===")
    for i, result in enumerate(results, 1):
        print(f"\n#{i} 相似度: {result['similarity']:.4f}")
        print(f"文件: {result['file']}")
        print(f"预览:\n{result['preview']}")
        print("-" * 50)

if __name__ == "__main__":
    main()