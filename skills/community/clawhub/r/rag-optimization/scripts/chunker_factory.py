# -*- coding: utf-8 -*-
"""
统一 Chunker 协议与策略路由
===========================
定义统一的 Chunk 数据结构与 chunk(document) 契约，让分块策略可热切换。

支持策略（与 config-template.json 的 chunking.strategies_available 一致）：
    fixed            定长分块（chunk_size/overlap）
    semantic         语义边界分块（按段落 + 句子边界，零依赖简化实现）
    small_to_big     由小到大：子块=句子，父块=段落
    proposition      命题分块（包装 proposition_chunker.py）
    contextual_header 上下文头增强分块（包装 contextual_header.py）

统一契约：
    chunker(document: str) -> List[Chunk]
    Chunk: {id, content, parent_paragraph, metadata}

运行 demo：
    python chunker_factory.py
"""
import logging
import re
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    """统一分块数据结构"""
    id: str                                   # 分块ID
    content: str                              # 分块内容（用于向量索引/检索）
    parent_paragraph: str = ""                # 父块（用于返回给 LLM 的完整上下文）
    metadata: Dict = field(default_factory=dict)  # 附加元数据（标题/章节/主题等）


# ----------------------------------------------------------------------
# 内置基础分块实现（纯标准库）
# ----------------------------------------------------------------------
    def to_document_unit(self) -> "DocumentUnit":
        """转换为统一 DocumentUnit 格式（Phase 1 数据协议集成）"""
        from document_unit import DocumentUnit
        return DocumentUnit(
            id=self.id,
            content=self.content,
            parent_paragraph=self.parent_paragraph,
            metadata=self.metadata,
        )



def _split_sentences(text: str) -> List[str]:
    """按中英文句末标点切分句子"""
    parts = re.split(r'(?<=[。！？.!?])\s*', text.strip())
    return [p.strip() for p in parts if p.strip()]


def _split_paragraphs(text: str) -> List[str]:
    """按空行切分段落"""
    return [p.strip() for p in re.split(r'\n\s*\n', text.strip()) if p.strip()]


def _chunk_fixed(document: str, config: Dict) -> List[Chunk]:
    """定长分块：chunk_size / overlap"""
    size = config.get('chunk_size', 500)
    overlap = config.get('overlap', 50)
    chunks = []
    start = 0
    n = len(document)
    i = 0
    while start < n:
        end = min(start + size, n)
        content = document[start:end].strip()
        if content:
            chunks.append(Chunk(id=f"fixed_{i}", content=content))
            i += 1
        if end >= n:
            break
        # H8：前进保护。overlap >= size 时 `end - overlap` 会 <= start，
        # 循环变量不前进 → 无限追加同一个块直到 OOM。
        # Bug 16 已给 small_to_big 的 step 加了同样的保护（见 _chunk_small_to_big），
        # 这里补上，两处共用 `max(步长, 1)` 这一同一规约。
        start = max(end - overlap, start + 1)
    return chunks


def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """计算两个向量的余弦相似度"""
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return max(0.0, min(1.0, dot / (norm_a * norm_b)))


def _chunk_semantic(document: str, config: Dict) -> List[Chunk]:
    """语义边界分块：优先使用向量嵌入计算句子相似度，按语义相似度切分。

    阶段说明：
        - 无 embedding_client 时：退化为结构性分块（段落+句子边界，纯标准库）
        - 有 embedding_client 时：使用真实语义相似度（similarity_threshold）
    """
    max_chunk = config.get('max_chunk_size', 1000)
    min_chunk = config.get('min_chunk_size', 100)
    similarity_threshold = config.get('similarity_threshold', 0.7)
    chunks = []
    i = 0

    # 尝试获取嵌入客户端
    embedding_client = config.get('_embedding_client')

    for para in _split_paragraphs(document):
        sentences = _split_sentences(para)
        if not sentences:
            continue

        if embedding_client:
            # === 语义相似度模式（使用真实向量） ===
            try:
                vectors = embedding_client.encode(sentences)
                # 按相似度聚合并块
                current_sentences = [sentences[0]]
                current_vectors = [vectors[0]]
                current_text = sentences[0]

                for j in range(1, len(sentences)):
                    sent = sentences[j]
                    vec = vectors[j]
                    # 计算当前句与 buffer 中最后一句的相似度
                    if current_vectors:
                        sim = _cosine_similarity(current_vectors[-1], vec)
                    else:
                        sim = 0.0

                    if sim >= similarity_threshold:
                        # 相似：合并到当前块
                        current_sentences.append(sent)
                        current_vectors.append(vec)
                        current_text += sent
                    else:
                        # 不相似：保存当前块，开新块
                        if len(current_text) >= min_chunk or len(current_sentences) >= 2:
                            chunks.append(Chunk(
                                id=f"semantic_{i}",
                                content=current_text.strip(),
                                parent_paragraph=para,
                            ))
                            i += 1
                        current_sentences = [sent]
                        current_vectors = [vec]
                        current_text = sent

                # 最后一个块：即使短于 min_chunk 也保留（避免丢失信息）
                if len(current_text) > 0:
                    chunks.append(Chunk(
                        id=f"semantic_{i}",
                        content=current_text.strip(),
                        parent_paragraph=para,
                    ))
                    i += 1
            except Exception as e:
                logger.warning(f"语义嵌入分块失败，降级为结构性分块: {e}")
                # 降级：走结构性模式
                buf = ""
                for sent in sentences:
                    if len(buf) + len(sent) <= max_chunk:
                        buf += sent
                    else:
                        if len(buf) >= min_chunk or len(buf.split()) >= 2:
                            chunks.append(Chunk(
                                id=f"semantic_{i}",
                                content=buf,
                                parent_paragraph=para,
                            ))
                            i += 1
                        buf = sent
                if len(buf) > 0:
                    chunks.append(Chunk(
                        id=f"semantic_{i}",
                        content=buf,
                        parent_paragraph=para,
                    ))
                    i += 1
        else:
            # === 结构性模式（无 embedding，纯标准库） ===
            buf = ""
            for sent in sentences:
                if len(buf) + len(sent) <= max_chunk:
                    buf += sent
                else:
                    if len(buf) >= min_chunk or len(buf.split()) >= 2:
                        chunks.append(Chunk(
                            id=f"semantic_{i}",
                            content=buf,
                            parent_paragraph=para,
                        ))
                        i += 1
                    buf = sent
            if len(buf) > 0:
                chunks.append(Chunk(
                    id=f"semantic_{i}",
                    content=buf,
                    parent_paragraph=para,
                ))
                i += 1

    return chunks


def _chunk_small_to_big(document: str, config: Dict) -> List[Chunk]:
    """由小到大：子块=句子/子句（用于检索），父块=段落聚合（用于生成）。

    父块聚合规则：优先使用 parent_chunk_size 将句子聚合为定长父块
    （达到 parent_chunk_size 即截断）；未配置 parent_chunk_size 时
    回退为自然段落作为父块。child_overlap 用于子句切分时的重叠。
    """
    child_max = config.get('child_chunk_size', 150)
    child_overlap = config.get('child_overlap', 0)
    parent_max = config.get('parent_chunk_size', 0)
    chunks = []
    i = 0
    for para in _split_paragraphs(document):
        sentences = _split_sentences(para)

        # 父块分组：按 parent_chunk_size 将句子聚合成多个父块；
        # 未配置时整段作为一个父块。
        groups = []  # [(parent_text, [sentence, ...])]
        if parent_max and parent_max > 0:
            buf, group_sents = "", []
            for sent in sentences:
                if buf and len(buf) + len(sent) > parent_max:
                    groups.append((buf, group_sents))
                    buf, group_sents = "", []
                buf += sent
                group_sents.append(sent)
            if buf:
                groups.append((buf, group_sents))
        else:
            groups = [(para, sentences)] if sentences else []

        # 子块：对每组父块内的句子切分子块，映射到该父块
        for parent, group_sents in groups:
            for sent in group_sents:
                step = max(child_max - child_overlap, 1)
                for k in range(0, len(sent), step):
                    sub = sent[k:k + child_max]
                    if sub.strip():
                        chunks.append(Chunk(
                            id=f"small_to_big_{i}",
                            content=sub,
                            parent_paragraph=parent,
                            metadata={'strategy': 'small_to_big'}
                        ))
                        i += 1
    return chunks


# ----------------------------------------------------------------------
# 包装已有分块器
# ----------------------------------------------------------------------
def _chunk_proposition(document: str, config: Dict) -> List[Chunk]:
    """包装 proposition_chunker.PropositionChunker"""
    from proposition_chunker import PropositionChunker
    chunker = PropositionChunker(config=config)
    props = chunker.chunk(document)
    return [
        Chunk(
            id=f"proposition_{j}",
            content=p.content,
            parent_paragraph=p.parent_paragraph,
            metadata={'is_atomic': p.is_atomic, 'is_self_contained': p.is_self_contained},
        )
        for j, p in enumerate(props)
    ]


def _chunk_contextual_header(document: str, config: Dict) -> List[Chunk]:
    """包装 contextual_header.ContextualHeaderEnhancer（无 LLM 时退回基础分块）"""
    try:
        from contextual_header import ContextualHeaderEnhancer
        enhancer = ContextualHeaderEnhancer(config=config)
        items = enhancer.enhance_document(document)
        chunks = []
        for j, item in enumerate(items):
            if isinstance(item, dict):
                content = item.get('text', item.get('enhanced_chunk', ''))
                header = item.get('header', {})
            else:
                content = str(item)
                header = {}
            chunks.append(Chunk(
                id=f"contextual_{j}",
                content=content,
                metadata={'header': header} if header else {},
            ))
        if chunks:
            return chunks
    except Exception as e:
        logger.warning(f"ContextualHeaderEnhancer 不可用（{e}），退回 semantic 分块")
    return _chunk_semantic(document, config)


# ----------------------------------------------------------------------
# 策略路由
# ----------------------------------------------------------------------
_STRATEGIES: Dict[str, Callable[[str, Dict], List[Chunk]]] = {
    'fixed': _chunk_fixed,
    'semantic': _chunk_semantic,
    'small_to_big': _chunk_small_to_big,
    'proposition': _chunk_proposition,
    'contextual_header': _chunk_contextual_header,
}


def get_chunker(strategy: str = 'small_to_big', config: Dict = None) -> Callable[[str], List[Chunk]]:
    """
    按策略名返回 chunker 函数。

    Args:
        strategy: fixed / semantic / small_to_big / proposition / contextual_header
        config: 分块配置（chunk_size、overlap、child_chunk_size 等）

    Returns:
        chunker(document: str) -> List[Chunk]
    """
    config = config or {}
    if strategy not in _STRATEGIES:
        raise ValueError(
            f"未知分块策略: {strategy}（可选: {', '.join(_STRATEGIES)}）"
        )
    impl = _STRATEGIES[strategy]
    return lambda document: impl(document, config)


def chunk_document(document: str, strategy: str = 'small_to_big', config: Dict = None) -> List[Chunk]:
    """便捷入口：切分单篇文档"""
    config = config or {}

    # 自动注入 embedding 客户端（仅对 semantic 策略有效）
    if strategy == 'semantic' and '_embedding_client' not in config:
        try:
            from llm_client import load_embedding_from_env
            emb_client = load_embedding_from_env()
            if emb_client:
                config['_embedding_client'] = emb_client
                logger.info(f"语义分块：自动加载 NVIDIA 嵌入模型")
        except Exception as e:
            logger.debug(f"自动加载嵌入模型失败，使用结构性分块: {e}")

    return get_chunker(strategy, config)(document)


if __name__ == '__main__':
    text = """第一章 产品概述
RAG（检索增强生成）是一种结合信息检索和生成模型的技术。它能够显著降低大模型的幻觉问题。
相比微调，RAG更新知识的成本更低，大约只有微调的十分之一。

第二章 优化策略
由小到大检索是RAG优化的核心策略之一。它的原理是用小块检索，返回大块上下文。
这种方法可以将准确率从0.3提升到0.85以上。它能够同时保证检索精度和上下文完整性。

第三章 高级话题
混合检索结合向量语义与BM25关键词匹配。短查询偏关键词，长查询偏语义。
重排序用Cross-Encoder对粗筛结果精排，可将准确率从0.5提升到0.7。"""

    for strategy in ['fixed', 'semantic', 'small_to_big', 'proposition', 'contextual_header']:
        chunks = chunk_document(text, strategy=strategy)
        print(f"\n=== [{strategy}] → {len(chunks)} 个块 ===")
        for c in chunks[:3]:
            print(f"  {c.id}: {c.content[:36]}...  parent={'有' if c.parent_paragraph else '无'}")
