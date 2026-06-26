#!/usr/bin/env python3
"""
知识库向量化索引脚本 (Ollama 版本)
使用 Ollama 的 embedding 模型将 knowledge 目录下的文档转换为向量并存储到 Chroma 数据库

使用方法:
    python index_knowledge_ollama.py [--knowledge-dir ./knowledge] [--output-dir ./vectorstore]
"""

import os
import sys
import argparse
import requests
import json
from pathlib import Path

# Windows 控制台 UTF-8 支持
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 检查依赖
try:
    from langchain_community.document_loaders import (
        DirectoryLoader,
        PyPDFLoader,
        UnstructuredMarkdownLoader,
        UnstructuredWordDocumentLoader,
    )
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    print("✓ LangChain 依赖已加载")
except ImportError as e:
    print(f"✗ 缺少依赖：{e}")
    print("\n请安装必要的包:")
    print("  pip install langchain langchain-community langchain-text-splitters chromadb pypdf unstructured python-docx")
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
        self._embeddings_cache = {}
    
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """批量获取文档的 embedding"""
        embeddings = []
        for i, text in enumerate(texts):
            print(f"  处理 {i+1}/{len(texts)}...", end='\r')
            emb = get_ollama_embedding(text, self.model)
            if emb:
                embeddings.append(emb)
            else:
                embeddings.append([0] * 1024)  # 返回零向量作为后备
        print(f"✓ 完成 {len(texts)} 个文档的 embedding")
        return embeddings
    
    def embed_query(self, text: str) -> list[float]:
        """获取单个查询的 embedding"""
        return get_ollama_embedding(text, self.model) or [0] * 1024


def load_documents(knowledge_dir: str):
    """加载知识库目录下的所有文档"""
    knowledge_path = Path(knowledge_dir)
    
    if not knowledge_path.exists():
        raise FileNotFoundError(f"知识库目录不存在：{knowledge_dir}")
    
    print(f"正在扫描知识库目录：{knowledge_path.absolute()}")
    
    # 统计文件
    files_found = {
        'pdf': 0, 'md': 0, 'txt': 0, 'docx': 0, 'xlsx': 0
    }
    
    for ext in ['**/*.pdf', '**/*.md', '**/*.txt', '**/*.docx', '**/*.xlsx']:
        count = len(list(knowledge_path.glob(ext)))
        files_found[ext.strip('**/*.')] = count
    
    total = sum(files_found.values())
    print(f"发现文件总数：{total}")
    for ext, count in files_found.items():
        if count > 0:
            print(f"  - .{ext}: {count} 个")
    
    # 加载文档
    documents = []
    
    # 加载 PDF
    pdf_files = list(knowledge_path.glob("**/*.pdf"))
    if pdf_files:
        print(f"\n正在加载 {len(pdf_files)} 个 PDF 文件...")
        for pdf_file in pdf_files:
            try:
                loader = PyPDFLoader(str(pdf_file))
                docs = loader.load()
                for doc in docs:
                    doc.metadata['source'] = str(pdf_file.relative_to(knowledge_path))
                documents.extend(docs)
                print(f"  ✓ {pdf_file.relative_to(knowledge_path)}")
            except Exception as e:
                print(f"  ✗ {pdf_file.name}: {e}")
    
    # 加载 Markdown
    md_files = list(knowledge_path.glob("**/*.md"))
    if md_files:
        print(f"\n正在加载 {len(md_files)} 个 Markdown 文件...")
        for md_file in md_files:
            try:
                loader = UnstructuredMarkdownLoader(str(md_file))
                docs = loader.load()
                for doc in docs:
                    doc.metadata['source'] = str(md_file.relative_to(knowledge_path))
                documents.extend(docs)
                print(f"  ✓ {md_file.relative_to(knowledge_path)}")
            except Exception as e:
                print(f"  ✗ {md_file.name}: {e}")
    
    # 加载 TXT
    txt_files = list(knowledge_path.glob("**/*.txt"))
    if txt_files:
        print(f"\n正在加载 {len(txt_files)} 个 TXT 文件...")
        for txt_file in txt_files:
            try:
                loader = DirectoryLoader(
                    str(txt_file.parent),
                    glob=str(txt_file.name),
                    loader_cls=UnstructuredMarkdownLoader
                )
                docs = loader.load()
                documents.extend(docs)
                print(f"  ✓ {txt_file.relative_to(knowledge_path)}")
            except Exception as e:
                print(f"  ✗ {txt_file.name}: {e}")
    
    # 加载 Word 文档
    docx_files = list(knowledge_path.glob("**/*.docx"))
    if docx_files:
        print(f"\n正在加载 {len(docx_files)} 个 Word 文档...")
        for docx_file in docx_files:
            try:
                loader = UnstructuredWordDocumentLoader(str(docx_file))
                docs = loader.load()
                for doc in docs:
                    doc.metadata['source'] = str(docx_file.relative_to(knowledge_path))
                documents.extend(docs)
                print(f"  ✓ {docx_file.relative_to(knowledge_path)}")
            except Exception as e:
                print(f"  ✗ {docx_file.name}: {e}")
    
    print(f"\n✓ 成功加载 {len(documents)} 个文档片段")
    return documents, knowledge_path


def split_documents(documents, chunk_size=500, chunk_overlap=50):
    """将文档分割为小块"""
    print(f"\n正在进行文本分块 (chunk_size={chunk_size}, overlap={chunk_overlap})...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", "。", "！", "？", "；", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"✓ 分块完成：{len(chunks)} 个片段")
    return chunks


def create_vectorstore(chunks, embeddings, output_dir: str):
    """创建向量数据库"""
    output_path = Path(output_dir)
    
    print(f"\n正在创建向量数据库...")
    print(f"存储路径：{output_path.absolute()}")
    
    # 创建或加载向量库
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(output_path),
        collection_name="knowledge_base"
    )
    
    print(f"\n✓ 向量数据库创建成功!")
    print(f"  - 文档片段：{len(chunks)} 个")
    print(f"  - 模型：nomic-embed-text-v2-moe (Ollama)")
    print(f"  - 存储位置：{output_path.absolute()}")
    
    return vectorstore


def main():
    parser = argparse.ArgumentParser(description="知识库向量化索引工具 (Ollama 版本)")
    parser.add_argument(
        "--knowledge-dir", "-k",
        default="./knowledge",
        help="知识库目录路径 (默认：./knowledge)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="./vectorstore",
        help="向量数据库输出目录 (默认：./vectorstore)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="文本分块大小 (默认：500)"
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=50,
        help="文本分块重叠 (默认：50)"
    )
    parser.add_argument(
        "--model",
        default="nomic-embed-text-v2-moe",
        help="Ollama embedding 模型 (默认：nomic-embed-text-v2-moe)"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="强制重建向量库 (删除已有数据)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("📚 OpenClaw RAG 知识库索引工具 (Ollama 版本)")
    print("=" * 60)
    print(f"使用模型：{args.model}")
    
    # 检查 Ollama 连接
    print("\n检查 Ollama 服务...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✓ Ollama 服务正常运行")
        else:
            print("✗ Ollama 服务响应异常")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到 Ollama 服务")
        print("  请先启动 Ollama: ollama serve")
        sys.exit(1)
    
    # 检查是否强制重建
    output_path = Path(args.output_dir)
    if output_path.exists() and args.rebuild:
        print(f"\n⚠️  检测到已有向量库，正在删除...")
        import shutil
        shutil.rmtree(output_path)
        print("✓ 已清理旧数据")
    elif output_path.exists():
        print(f"\n⚠️  检测到已有向量库：{output_path.absolute()}")
        print("   如需重建，请添加 --rebuild 参数")
        print("   本次将在现有基础上追加索引")
    
    try:
        # 1. 加载文档
        documents, knowledge_path = load_documents(args.knowledge_dir)
        
        if not documents:
            print("\n✗ 未找到任何可索引的文档!")
            print("   支持格式：.pdf, .md, .txt, .docx")
            sys.exit(1)
        
        # 2. 分割文档
        chunks = split_documents(
            documents,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap
        )
        
        # 3. 创建 Ollama Embedding 适配器
        print(f"\n初始化 Ollama Embedding ({args.model})...")
        embeddings = OllamaEmbeddings(model=args.model)
        
        # 4. 创建向量库
        vectorstore = create_vectorstore(chunks, embeddings, args.output_dir)
        
        # 5. 保存配置信息
        config = {
            "knowledge_dir": str(knowledge_path.absolute()),
            "vectorstore_dir": str(output_path.absolute()),
            "chunk_size": args.chunk_size,
            "chunk_overlap": args.chunk_overlap,
            "embedding_model": f"ollama/{args.model}",
            "document_count": len(documents),
            "chunk_count": len(chunks)
        }
        
        config_file = output_path / "index_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"\n✓ 配置已保存：{config_file}")
        
        print("\n" + "=" * 60)
        print("✅ 索引完成！现在可以使用 RAG 进行智能检索了")
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"\n✗ 索引失败：{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 索引失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
