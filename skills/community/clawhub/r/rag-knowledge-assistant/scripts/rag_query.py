#!/usr/bin/env python3
"""
RAG 向量检索脚本
使用向量相似度搜索知识库中的相关内容

使用方法:
    python rag_query.py "你的问题" [--vectorstore ./vectorstore] [--top-k 5]
"""

import os
import sys
import argparse
import json
from pathlib import Path

# Windows 控制台 UTF-8 支持
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 检查依赖
try:
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    print("✓ LangChain 依赖已加载")
except ImportError as e:
    print(f"✗ 缺少依赖：{e}")
    print("\n请安装必要的包:")
    print("  pip install langchain langchain-community chromadb")
    sys.exit(1)


def load_vectorstore(vectorstore_dir: str):
    """加载已有的向量数据库"""
    vectorstore_path = Path(vectorstore_dir)
    
    if not vectorstore_path.exists():
        raise FileNotFoundError(
            f"向量数据库不存在：{vectorstore_dir}\n"
            "请先运行 index_knowledge.py 创建索引"
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
    
    print(f"\n正在加载向量数据库：{vectorstore_path.absolute()}...")
    
    # 加载 Embedding 模型
    print("加载 Embedding 模型 (BAAI/bge-m3)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    
    # 加载向量库
    vectorstore = Chroma(
        persist_directory=str(vectorstore_path),
        embedding_function=embeddings,
        collection_name="knowledge_base"
    )
    
    print("✓ 向量数据库加载成功")
    return vectorstore, embeddings


def similarity_search(vectorstore, query: str, top_k: int = 5, score_threshold: float = 0.6):
    """执行相似度搜索"""
    print(f"\n🔍 检索问题：{query}")
    print(f"   返回数量：top_k={top_k}, 阈值={score_threshold}")
    
    # 执行搜索
    results = vectorstore.similarity_search_with_score(query, k=top_k)
    
    # 过滤低相似度结果
    filtered_results = []
    for doc, score in results:
        similarity = 1 - score  # 转换为相似度分数
        if similarity >= score_threshold:
            filtered_results.append((doc, score))
    
    print(f"\n✓ 找到 {len(filtered_results)} 个相关片段")
    
    return filtered_results


def format_results(results, include_metadata: bool = True):
    """格式化搜索结果"""
    output = []
    
    for i, (doc, score) in enumerate(results, 1):
        similarity = 1 - score
        output.append(f"\n{'='*60}")
        output.append(f"📄 结果 #{i} (相似度：{similarity:.2%})")
        output.append(f"{'='*60}")
        
        if include_metadata:
            source = doc.metadata.get('source', '未知来源')
            output.append(f"来源：{source}")
            if 'page' in doc.metadata:
                output.append(f"页码：{doc.metadata['page']}")
        
        output.append(f"\n{doc.page_content}")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="RAG 向量检索工具")
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
        "--score-threshold", "-t",
        type=float,
        default=0.6,
        help="相似度阈值 (默认：0.6)"
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
    print("🤖 OpenClaw RAG 智能检索")
    print("=" * 60)
    
    try:
        # 加载向量库
        vectorstore, embeddings = load_vectorstore(args.vectorstore)
        
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
                        score_threshold=args.score_threshold
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
                score_threshold=args.score_threshold
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
