#!/usr/bin/env python3
"""
Smart Cache Embeddings - 向量嵌入工具
支持 OpenAI embedding API 和本地模型
"""

import os
import json
import math
from typing import List, Optional, Tuple
from pathlib import Path


def load_config() -> dict:
    """加载配置文件"""
    config_path = Path.home() / ".qclaw" / "smart-cache" / "config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def get_embedding_model() -> str:
    """获取配置的 embedding 模型"""
    config = load_config()
    return config.get("embedding_model", "text-embedding-3-small")


def get_api_key() -> Optional[str]:
    """获取 API Key"""
    # 优先级：环境变量 > 配置文件
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("DASHSCOPE_API_KEY")
    if api_key:
        return api_key

    config_path = Path.home() / ".qclaw" / "smart-cache" / "config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get("api_key") or config.get("openai_api_key")

    return None


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """计算两个向量的余弦相似度"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


class EmbeddingsProvider:
    """
    向量嵌入提供者基类
    """

    def get_embedding(self, text: str) -> Optional[List[float]]:
        raise NotImplementedError

    def get_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        raise NotImplementedError


class OpenAIEmbeddings(EmbeddingsProvider):
    """
    OpenAI Embedding API
    支持模型: text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"):
        self.api_key = api_key or get_api_key()
        self.model = model

        if not self.api_key:
            raise ValueError(
                "未找到 API Key。请设置环境变量 OPENAI_API_KEY "
                "或在 config.json 中配置 api_key"
            )

    def get_embedding(self, text: str) -> Optional[List[float]]:
        """获取单条文本的嵌入向量"""
        result = self.get_embeddings([text])
        return result[0] if result else None

    def get_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        """批量获取文本嵌入向量"""
        import urllib.request
        import urllib.error

        url = "https://api.openai.com/v1/embeddings"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.model,
            "input": texts
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return [item["embedding"] for item in result["data"]]
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"OpenAI API 错误: {e.code} - {error_body}")
            return None
        except Exception as e:
            print(f"请求错误: {e}")
            return None


class DashScopeEmbeddings(EmbeddingsProvider):
    """
    阿里云 DashScope Embedding API
    支持模型: text-embedding-v1, text-embedding-v2
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-v1"):
        self.api_key = api_key or os.environ.get("DASHSCOPE_API_KEY")
        self.model = model

        if not self.api_key:
            raise ValueError(
                "未找到 DashScope API Key。请设置环境变量 DASHSCOPE_API_KEY"
            )

    def get_embedding(self, text: str) -> Optional[List[float]]:
        """获取单条文本的嵌入向量"""
        result = self.get_embeddings([text])
        return result[0] if result else None

    def get_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        """批量获取文本嵌入向量"""
        import urllib.request
        import urllib.error

        url = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.model,
            "input": {"messages": [{"text": text} for text in texts]}
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                embeddings = result.get("output", {}).get("embeddings", [])
                return [item["embedding"] for item in embeddings]
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"DashScope API 错误: {e.code} - {error_body}")
            return None
        except Exception as e:
            print(f"请求错误: {e}")
            return None


class LocalEmbeddings(EmbeddingsProvider):
    """
    本地 embedding 模型（使用 sentence-transformers）
    需要安装: pip install sentence-transformers
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except ImportError:
                raise ImportError(
                    "本地模型需要安装 sentence-transformers: pip install sentence-transformers"
                )

    def get_embedding(self, text: str) -> Optional[List[float]]:
        """获取单条文本的嵌入向量"""
        self._load_model()
        embedding = self._model.encode(text)
        return embedding.tolist()

    def get_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        """批量获取文本嵌入向量"""
        self._load_model()
        embeddings = self._model.encode(texts)
        return embeddings.tolist()


def create_embeddings_provider(provider: str = "openai", **kwargs) -> EmbeddingsProvider:
    """
    工厂函数：创建嵌入提供者

    Args:
        provider: 提供者类型 "openai", "dashscope", "local"
        **kwargs: 传递给提供者的参数

    Returns:
        EmbeddingsProvider 实例
    """
    providers = {
        "openai": OpenAIEmbeddings,
        "dashscope": DashScopeEmbeddings,
        "local": LocalEmbeddings,
    }

    if provider not in providers:
        raise ValueError(f"不支持的提供者: {provider}。可用: {list(providers.keys())}")

    return providers[provider](**kwargs)


# 便捷函数
def get_text_embedding(text: str, provider: str = "openai", **kwargs) -> Optional[List[float]]:
    """
    获取单条文本的嵌入向量

    Args:
        text: 文本内容
        provider: 提供者 "openai", "dashscope", "local"
        **kwargs: 额外参数

    Returns:
        嵌入向量列表，失败返回 None
    """
    try:
        emb_provider = create_embeddings_provider(provider, **kwargs)
        return emb_provider.get_embedding(text)
    except Exception as e:
        print(f"获取 embedding 失败: {e}")
        return None


def compute_similarity(text1: str, text2: str, provider: str = "openai") -> float:
    """
    计算两条文本的语义相似度

    Args:
        text1: 文本1
        text2: 文本2
        provider: 提供者类型

    Returns:
        相似度分数 [0, 1]
    """
    emb1 = get_text_embedding(text1, provider)
    emb2 = get_text_embedding(text2, provider)

    if emb1 is None or emb2 is None:
        return 0.0

    return cosine_similarity(emb1, emb2)


def find_similar(
    query: str,
    texts: List[str],
    threshold: float = 0.85,
    provider: str = "openai"
) -> List[Tuple[int, str, float]]:
    """
    在文本列表中查找与查询相似的文本

    Args:
        query: 查询文本
        texts: 候选文本列表
        threshold: 相似度阈值
        provider: 提供者类型

    Returns:
        [(索引, 文本, 相似度), ...]，按相似度降序排列
    """
    query_emb = get_text_embedding(query, provider)
    if query_emb is None:
        return []

    results = []
    for i, text in enumerate(texts):
        text_emb = get_text_embedding(text, provider)
        if text_emb is None:
            continue

        similarity = cosine_similarity(query_emb, text_emb)
        if similarity >= threshold:
            results.append((i, text, similarity))

    results.sort(key=lambda x: x[2], reverse=True)
    return results


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("用法: python embeddings.py <命令> [参数]")
        print("命令:")
        print("  embed <文本>           - 获取文本的嵌入向量")
        print("  similarity <文本1> <文本2> - 计算两条文本的相似度")
        print("  provider              - 查看当前配置的 provider")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "provider":
        config = load_config()
        print(f"当前 embedding provider: {config.get('embedding_provider', 'openai')}")
        print(f"当前模型: {get_embedding_model()}")
        api_key = get_api_key()
        if api_key:
            print(f"API Key: {'*' * 20}{api_key[-4:]}")
        else:
            print("API Key: 未配置")

    elif cmd == "embed":
        if len(sys.argv) < 3:
            print("用法: python embeddings.py embed <文本>")
            sys.exit(1)
        text = sys.argv[2]
        embedding = get_text_embedding(text)
        if embedding:
            print(f"维度: {len(embedding)}")
            print(f"前5维: {embedding[:5]}")
        else:
            print("获取 embedding 失败")

    elif cmd == "similarity":
        if len(sys.argv) < 4:
            print("用法: python embeddings.py similarity <文本1> <文本2>")
            sys.exit(1)
        text1, text2 = sys.argv[2], sys.argv[3]
        sim = compute_similarity(text1, text2)
        print(f"相似度: {sim:.4f}")

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
