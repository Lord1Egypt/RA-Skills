#!/usr/bin/env python3
"""
RAG 向量检索脚本 (Ollama 版本)
使用 Ollama embedding 模型进行向量相似度搜索

使用方法:
    python rag_query_ollama.py "你的问题" [--vectorstore ./vectorstore] [--top-k 5]
"""

import os
import sys
import argparse
import json
import requests
from pathlib import Path

# Windows 控制台 UTF-8 支持
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 检查依赖
try:
    from langchain_community.vectorstores import Chroma
    print("✓ LangChain 依赖已加载")
except ImportError as e:
    print(f"✗ 缺少依赖：{e}")
    print("\n请安装必要的包:")
    print("  pip install langchain langchain-community chromadb")
    sys.exit(1)


def get_ollama_embedding(text: str, model: str = "nomic-embed-text-v2-moe"):
    """使用 Ollama API 获取文本的 embedding"""
    url = "http://localhost:11434/api/embeddings"
    
    payload = {
        "model": model,
        "prompt": text
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["embedding"]
    except requests.exceptions.ConnectionError:
        print("✗ 错误：无法连接到 Ollama (http://localhost:11434)")
        print("  请确保 Ollama 服务正在运行：ollama serve")
        sys.exit(1)
    except Exception as e:
        print(f"✗ 获取 embedding 失败：{e}")
        return None


class OllamaEmbeddings:
    """Ollama Embedding 适配器"""
    
    def __init__(self, model: str = "nomic-embed-text-v2-moe"):
        self.model = model
    
    def embed_query(self, text: str) -> list[float]:
        """获取单个查询的 embedding"""
        return get_ollama_embedding(text, self.model) or [0] * 1024


def load_vectorstore(vectorstore_dir: str, model: str = "nomic-embed-text-v2-moe"):
    """加载已有的向量数据库"""
    vectorstore_path = Path(vectorstore_dir)
    
    if not vectorstore_path.exists():
        raise FileNotFoundError(
            f"向量数据库不存在：{vectorstore_dir}\n"
            "请先运行 index_knowledge_ollama.py 创建索引"
        )
    
    # 检查配置文件
    config_file = vectorstore_path / "index_config.json"
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✓ 加载配置：{config_file}")
        print(f"  - 知识库：{config.get('knowledge_dir', '未知')}")
        print(f"  - 文档数：{config.get('document_count', 0)}")
        print(f"  - 片段数：{config.get('chunk_count', 0)}")
        print(f"  - 模型：{config.get('embedding_model', '未知')}")
    
    print(f"\n正在加载向量数据库：{vectorstore_path.absolute()}...")
    
    # 加载 Ollama Embedding 模型
    print(f"加载 Ollama Embedding 模型 ({model})...")
    embeddings = OllamaEmbeddings(model=model)
    
    # 加载向量库
    vectorstore = Chroma(
        persist_directory=str(vectorstore_path),
        embedding_function=embeddings,
        collection_name="knowledge_base"
    )
    
    print("✓ 向量数据库加载成功")
    return vectorstore, embeddings


def similarity_search(vectorstore, query: str, top_k: int = 5, distance_threshold: float = 200.0):
    """执行相似度搜索
    
    Chroma 使用 L2 距离，距离越小越相似。
    典型 L2 距离范围：0 (完全相同) 到 500+ (完全不同)
    建议阈值：150-200 用于宽松匹配，100-150 用于严格匹配
    """
    print(f"\n🔍 检索问题：{query}")
    print(f"   返回数量：top_k={top_k}, 距离阈值={distance_threshold}")
    
    # 执行搜索
    results = vectorstore.similarity_search_with_score(query, k=top_k)
    
    # 过滤高距离结果（距离越小越相似）
    filtered_results = []
    for doc, distance in results:
        if distance <= distance_threshold:
            filtered_results.append((doc, distance))
    
    print(f"\n✓ 找到 {len(filtered_results)} 个相关片段")
    
    return filtered_results


def format_results(results, include_metadata: bool = True):
    """格式化搜索结果"""
    output = []
    
    for i, (doc, distance) in enumerate(results, 1):
        # L2 距离，越小越相似
        output.append(f"\n{'='*60}")
        output.append(f"📄 结果 #{i} (L2 距离：{distance:.2f})")
        output.append(f"{'='*60}")
        
        if include_metadata:
            source = doc.metadata.get('source', '未知来源')
            output.append(f"来源：{source}")
        
        output.append(f"\n{doc.page_content}")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="RAG 向量检索工具 (Ollama 版本)")
    parser.add_argument(
        "query",
        nargs="?",
        help="检索问题"
    )
    parser.add_argument(
        "--vectorstore", "-v",
        default="./vectorstore",
        help="向量数据库目录 (默认：./vectorstore)"
    )
    parser.add_argument(
        "--top-k", "-k",
        type=int,
        default=5,
        help="返回结果数量 (默认：5)"
    )
    parser.add_argument(
        "--distance-threshold", "-t",
        type=float,
        default=200.0,
        help="L2 距离阈值 (默认：200.0，越小越严格)"
    )
    parser.add_argument(
        "--model", "-m",
        default="nomic-embed-text-v2-moe",
        help="Ollama embedding 模型 (默认：nomic-embed-text-v2-moe)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出结果"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="交互模式 (连续问答)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🤖 OpenClaw RAG 智能检索 (Ollama 版本)")
    print("=" * 60)
    
    try:
        # 加载向量库
        vectorstore, embeddings = load_vectorstore(args.vectorstore, args.model)
        
        # 交互模式
        if args.interactive or not args.query:
            print("\n💬 进入交互模式 (输入 'quit' 退出)")
            print("-" * 60)
            
            while True:
                try:
                    query = input("\n你的问题：").strip()
                    if query.lower() in ['quit', 'exit', 'q']:
                        print("再见！")
                        break
                    if not query:
                        continue
                    
                    results = similarity_search(
                        vectorstore,
                        query,
                        top_k=args.top_k,
                        distance_threshold=args.distance_threshold
                    )
                    
                    if results:
                        print(format_results(results))
                    else:
                        print("\n⚠️  未找到足够相关的信息")
                        print("   建议：尝试更具体的关键词或降低阈值")
                
                except KeyboardInterrupt:
                    print("\n\n再见！")
                    break
            return
        
        # 单次查询模式
        if args.query:
            results = similarity_search(
                vectorstore,
                args.query,
                top_k=args.top_k,
                distance_threshold=args.distance_threshold
            )
            
            if args.json:
                # JSON 输出
                output = {
                    "query": args.query,
                    "results": [
                        {
                            "rank": i,
                            "similarity": float(1 - score),
                            "source": doc.metadata.get('source', 'unknown'),
                            "content": doc.page_content
                        }
                        for i, (doc, score) in enumerate(results, 1)
                    ]
                }
                print(json.dumps(output, ensure_ascii=False, indent=2))
            else:
                # 文本输出
                print(format_results(results))
            
            if not results:
                print("\n⚠️  未找到足够相关的信息")
                print("   建议：尝试更具体的关键词或降低阈值")
        
    except FileNotFoundError as e:
        print(f"\n✗ 错误：{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 检索失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
