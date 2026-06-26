# 大模型RAG实战｜混合检索：BM25检索+向量检索的LlamaIndex实现

原文链接：https://mp.weixin.qq.com/s/_5p1qhLrxlh0HxX3uazhSg?token=1267526467&lang=zh_CN

ThinkRAG 大模型 RAG 实战系列文章，带你深入探索使用 LlamaIndex 框架，构建本地大模型知识库问答系统。本系列涵盖知识库管理、检索优化、模型本地部署等主题，通过代码与实例，讲解如何打造生产级系统，实现本地知识库的快速检索与智能问答。

此前，我介绍了使用 Elasticsearch 实现混合检索。本文我将介绍一种效果更好的混合检索方法，在实际问答场景中，优于向量数据库自带的混合检索功能。

## 1 什么是混合检索

目前，大模型 RAG 系统中普遍采用混合检索来提升检索准确性。针对要回答的问题，同时通过向量语义相似度检索以及基于关键词的全文检索，将检索到的文本块进行融合处理（包括去重与排序），然后再把得分最高的文本块给到大模型生成回答。这，就是混合检索的原理。

通过引入向量数据库，比如 Chroma, LanceDB 或者上篇文章中提到的 Elasticsearch，我们可以非常容易地实现向量检索。所以，当我们要实现混合检索，一个问题就在于如何实现全文检索。好在 LlamaIndex 提供了实现 BM25 检索的方法。

## 2 构建 BM25 检索器

BM25 是一种文本相关度检索方法，主要是判断一个文档和查询语句匹配的程度的算法，比如在搜索引擎中用于排序搜索结果。这种文本相关度的判断，主要基于词语权重和文档权重的融合：

- 词频 TF（Term Frequency）：一个词在一个文档中出现的频率越高，那么文档的相关性也越高。
- 逆向文档频率 IDF（Inverse Document Frequency）：每个词在索引中出现的频率越高，相关性越低。IDF 主要是为了降低像“的”这样高频词语的相关性，提升包含低频专业术语的文档的权重。

这两者结合起来就形成了 TF-IDF 算法。BM25 算法则基于 TF-IDF 作了优化，主要是降低长文档的权重。

LlamaIndex 实现了 BM25 算法的检索器：BM25Retriever【参考资料 1】。不过，BM25Retriever 默认使用的 tokenizer 不支持中文，所以我们使用 Jieba 作为 tokenizer。这样，我们定制一个适合中文的 BM25 检索器 SimpleBM25Retriever：

```python
import jieba
from typing import List

def chinese_tokenizer(text: str) -> List[str]:
    return list(jieba.cut(text))

class SimpleBM25Retriever(BM25Retriever):
    @classmethod
    def from_defaults(cls, index, similarity_top_k, **kwargs) -> "BM25Retriever":
        docstore = index.docstore
        return BM25Retriever.from_defaults(
            docstore=docstore,
            similarity_top_k=similarity_top_k,
            verbose=True,
            tokenizer=chinese_tokenizer,
            **kwargs,
        )
```

考虑到使用向量检索时，我们通常基于 index 构建向量检索器。同样，以上定制的 BM25 检索器，我们也将 index 作为参数载入，然后在构建 BM25Retriever 时，将 index.docstore 传递过去。BM25 检索的内容基于 LlamaIndex 框架中的文档存储（docstore）。

我在之前的文章中提到，可以采用 MongoDB 作为文档存储（doc store）和索引存储（index store）。一个更好的选择就是使用 Redis【参考资料 2】，它还可以作为文本提取管道的缓存（ingestion cache）和问答记录存储（chat store）。这样，我们在一个 RAG 系统中，就不需要引入太多不同种类的数据库。

## 3 实现混合检索

接下来，我们需要把向量检索和 BM25 检索到的内容进行融合处理。LlamaIndex 提供了一个很好的方法：QueryFusionRetriever【参考资料 3】。

基于这个方法，我定制了一个新的类 SimpleFusionRetriever。首先，构建向量检索器（vector_retriever）和 BM25 检索器（bm25_retriever），然后构造 QueryFusionRetriever，并设置两者的权重分别为 0.6 和 0.4。这里，向量检索器的权重（0.6）更高，表明向量检索器的得分在最终排名中被认为更重要：

```python
class SimpleFusionRetriever(QueryFusionRetriever):
    def __init__(self, vector_index, top_k=2, mode=FUSION_MODES.DIST_BASED_SCORE):
        self.top_k = top_k
        self.mode = mode

        self.vector_retriever = VectorIndexRetriever(
            index=vector_index,
            similarity_top_k=top_k,
            verbose=True,
        )

        self.bm25_retriever = SimpleBM25Retriever.from_defaults(
            index=vector_index,
            similarity_top_k=top_k,
        )

        super().__init__(
            [self.vector_retriever, self.bm25_retriever],
            retriever_weights=[0.6, 0.4],
            similarity_top_k=top_k,
            num_queries=1,  # set this to 1 to disable query generation
            mode=mode,
            use_async=True,
            verbose=True,
        )
```

其中，融合处理的模式设置为 dist_based_score【参考资料 3】。LlamaIndex 目前支持以下四种模式：

```python
class FUSION_MODES(str, Enum):
    RECIPROCAL_RANK = "reciprocal_rerank"  # apply reciprocal rank fusion
    RELATIVE_SCORE = "relative_score"      # apply relative score fusion
    DIST_BASED_SCORE = "dist_based_score"  # apply distance-based score fusion
    SIMPLE = "simple"                      # simple re-ordering based on original scores
```

先介绍 relative_score，即相对得分融合算法（Relative Score Fusion），采用以下方法对检索内容进行处理：

- 最小-最大归一化：将每个检索器的得分归一化到一个共同的尺度上，通常在 0 到 1 之间。
- 加权求和：归一化后，得分使用加权求和的方式组合成一个最终得分。权重反映了每个检索器得分在最终排名中的相对重要性。

我们采用的 dist_based_score，是基于分布的得分融合算法（Distribution-Based Score Fusion）。作为 relative_score 的变体，它根据每个结果集的得分的均值和标准差来不同地进行归一化处理。这种方法考虑了不同检索器得分的分布特性，从而在融合时更加公平地对待每个检索器的得分。

QueryFusionRetriever 是一个很有趣的方法。它可以将原始的查询（query），通过 LLM 改写生成最多 4 个新的查询，然后对每一个检索器都逐一检索。也就是说，如果有 2 个检索器，那么一共进行 4 × 2 = 8 次检索。最终，该方法会对 8 次检索的内容，采用上述算法进行融合处理，去除重复的内容，并重新排序。

由于我们此次仅实验混合检索，而且不希望过多的 LLM 调用导致延迟响应，因此将参数 num_queries 设置为 1，不进行 query 的生成。

## 4 下一步做什么

本文介绍了使用 LlamaIndex 实现稠密向量检索 + BM25 全文检索的混合检索方法，属于 2 路召回。

值得注意的是，最近 IBM 的研究文章对比了各种检索方式的组合，并提出采用 Blended RAG【参考资料 4】，即使用 BM25 全文检索 + 稠密向量检索 + 稀疏向量检索的 3 路召回混合检索方法，可以达到更好地效果。后续，我将探索使用 LlamaIndex，实现 3 路召回混合检索，并向大家报告结果。

本文中的代码，都可以在 ThinkRAG【参考资料 5】这一开源项目中找到：

- https://github.com/wzdavid/ThinkRAG

参考资料：

1. https://docs.llamaindex.ai/en/stable/api_reference/retrievers/bm25/
2. https://docs.llamaindex.ai/en/stable/examples/docstore/RedisDocstoreIndexStoreDemo/
3. https://docs.llamaindex.ai/en/stable/examples/retrievers/relative_score_dist_fusion/
4. Blended RAG: Improving RAG (Retriever-Augmented Generation) Accuracy with Semantic Search and Hybrid Query-Based Retrievers, https://arxiv.org/abs/2404.07220 , 2024
5. https://github.com/wzdavid/ThinkRAG
