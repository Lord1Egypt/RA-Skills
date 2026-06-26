#!/usr/bin/env python3
"""
embed.py - Bedrock Titan Embeddings → OpenSearch

用法：
  # 索引一个页面
  python3 embed.py --page wiki/pages/aws/eks.md --index wiki-personal

  # 索引多个页面
  python3 embed.py --pages wiki/pages/aws/eks.md wiki/pages/ai/litellm.md --index wiki-personal

  # 向量搜索
  python3 embed.py --query "EKS 节点组配置" --index wiki-personal --top-k 5

  # 客户 wiki
  python3 embed.py --page wiki-clients/clientA/pages/xxx.md --index wiki-client-clientA
"""

import argparse
import json
import os
import sys
import boto3
from datetime import datetime

REGION = os.environ.get("AWS_REGION", "us-east-1")
SECRET_NAME = os.environ.get("WIKI_EMBED_SECRET", "wikisage/opensearch")
WORKSPACE = os.environ.get("WIKI_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))


def get_opensearch_config():
    sm = boto3.client("secretsmanager", region_name=REGION)
    secret = sm.get_secret_value(SecretId=SECRET_NAME)
    return json.loads(secret["SecretString"])


def get_embedding(text: str) -> list:
    bedrock = boto3.client("bedrock-runtime", region_name=REGION)
    body = json.dumps({"inputText": text[:8000]})  # Titan v2 max 8192 tokens
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    result = json.loads(response["body"].read())
    return result["embedding"]


def ensure_index(os_client, index_name: str):
    """创建 index（如果不存在）"""
    from opensearchpy import OpenSearch, RequestsHttpConnection
    if not os_client.indices.exists(index=index_name):
        mapping = {
            "settings": {"index": {"knn": True}},
            "mappings": {
                "properties": {
                    "page": {"type": "keyword"},
                    "content": {"type": "text"},
                    "embedding": {
                        "type": "knn_vector",
                        "dimension": 1024,  # Titan v2 default
                        "method": {
                            "name": "hnsw",
                            "space_type": "cosinesimil",
                            "engine": "nmslib",
                        },
                    },
                    "category": {"type": "keyword"},
                    "updated_at": {"type": "date"},
                }
            },
        }
        os_client.indices.create(index=index_name, body=mapping)
        print(f"✅ 创建 index: {index_name}")


def index_page(os_client, index_name: str, page_path: str):
    """索引单个页面"""
    full_path = os.path.join(WORKSPACE, page_path) if not os.path.isabs(page_path) else page_path
    with open(full_path, "r") as f:
        content = f.read()

    # 判断分类
    category = "general"
    for cat in ["aws", "ai", "projects", "ops"]:
        if f"/{cat}/" in page_path:
            category = cat
            break

    print(f"📄 生成 embedding: {page_path}")
    embedding = get_embedding(content)

    doc = {
        "page": page_path,
        "content": content,
        "embedding": embedding,
        "category": category,
        "updated_at": datetime.utcnow().isoformat(),
    }

    os_client.index(index=index_name, id=page_path, body=doc)
    print(f"✅ 已索引: {page_path}")


def search(os_client, index_name: str, query: str, top_k: int = 5):
    """向量搜索"""
    print(f"🔍 搜索: {query}")
    embedding = get_embedding(query)

    search_body = {
        "size": top_k,
        "query": {
            "knn": {
                "embedding": {
                    "vector": embedding,
                    "k": top_k,
                }
            }
        },
        "_source": ["page", "content", "category"],
    }

    response = os_client.search(index=index_name, body=search_body)
    hits = response["hits"]["hits"]

    results = []
    for hit in hits:
        results.append({
            "page": hit["_source"]["page"],
            "score": hit["_score"],
            "category": hit["_source"].get("category", ""),
            "preview": hit["_source"]["content"][:200],
        })

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", help="单个页面路径")
    parser.add_argument("--pages", nargs="+", help="多个页面路径")
    parser.add_argument("--query", help="搜索查询")
    parser.add_argument("--index", required=True, help="OpenSearch index 名")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    # 获取 OpenSearch 配置
    config = get_opensearch_config()
    endpoint = config["endpoint"]
    if not endpoint:
        print(f"❌ OpenSearch endpoint 未配置，请更新 Secrets Manager: {SECRET_NAME}")
        sys.exit(1)

    # 去掉 https:// 前缀
    host = endpoint.replace("https://", "").rstrip("/")

    from opensearchpy import OpenSearch, RequestsHttpConnection
    from requests_aws4auth import AWS4Auth

    # 使用 basic auth（Fine-grained access control）
    os_client = OpenSearch(
        hosts=[{"host": host, "port": 443}],
        http_auth=(config["username"], config["password"]),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )

    # 确保 index 存在
    ensure_index(os_client, args.index)

    if args.query:
        results = search(os_client, args.index, args.query, args.top_k)
        print(json.dumps(results, ensure_ascii=False, indent=2))

    elif args.page:
        index_page(os_client, args.index, args.page)

    elif args.pages:
        for page in args.pages:
            index_page(os_client, args.index, page)

    else:
        print("❌ 请指定 --page、--pages 或 --query")
        sys.exit(1)


if __name__ == "__main__":
    main()
