# Attribution — 版权声明与许可说明

> 本技能包含第三方开源组件和预训练模型，各自遵循不同的许可协议。
> 技能代码本身采用 MIT 协议，见 `references/LICENSE.md`。

---

## 一、本技能代码

- **许可协议**：MIT License
- **版权归属**：Copyright (c) 2026 wUwproject
- **文件范围**：`SKILL.md`、`scripts/*.py`、`references/*.md`（除本文件所列第三方内容外）

---

## 二、使用到的 Python 依赖库

以下库通过 `pip install` 自动安装，其许可协议与本技能代码各自独立：

| 库 | 安装名 | 许可协议 | 版权方 |
|:--|:-----:|:--------:|--------|
| Sentence-Transformers | `sentence-transformers` | Apache 2.0 | UKP Lab, TU Darmstadt / Hugging Face |
| 🤗 Transformers | `transformers` | Apache 2.0 | Hugging Face Inc. |
| 🤗 Hub | `huggingface-hub` | Apache 2.0 | Hugging Face Inc. |

> Pipeline B 为纯正则实现（5W2H/主语/约束/分块），不依赖第三方 NLP 库。

---

## 三、Pipeline A — 嵌入与重排序模型

### BAAI/bge-small-zh-v1.5（嵌入层）

| 项目 | 内容 |
|:----|:----|
| **许可协议** | **MIT License** ✅ 商业友好 |
| **版权方** | 北京智源人工智能研究院（BAAI） |
| **项目地址** | https://github.com/FlagOpen/FlagEmbedding |
| **许可原文** | https://github.com/FlagOpen/FlagEmbedding/blob/master/LICENSE |
| **大小** | ~92MB |
| **用途** | Pipeline A 嵌入层：文本向量化与余弦相似度匹配 |

### BAAI/bge-reranker-base（CrossEncoder 重排序层）

| 项目 | 内容 |
|:----|:----|
| **许可协议** | **MIT License** ✅ 商业友好 |
| **版权方** | 北京智源人工智能研究院（BAAI） |
| **项目地址** | https://github.com/FlagOpen/FlagEmbedding |
| **许可原文** | https://github.com/FlagOpen/FlagEmbedding/blob/master/LICENSE |
| **大小** | ~1.1GB |
| **用途** | Pipeline A CrossEncoder 层：query-doc 相关性重排序（基于 BERT 架构） |

---

## 四、Pipeline B — 结构分析

Pipeline B 为纯正则实现，不依赖第三方模型。覆盖 5W2H 提取、主语识别、约束标注、分块、注意力锚定。

---

## 五、Pipeline C — 智能体推理

Pipeline C 不依赖外部模型或 API。推理由智能体（AI Agent）原生完成，无需额外配置。

- 技能输出 `agent_context`（含 5W2H、约束标注、结构分析、模板参考）
- 智能体读取该上下文后自行执行聚焦/发散/整合推理
- 推理结果自动通用化并保存为能力级 JSON 模板（自增强闭环）

---

## 六、总结

| 组件 | 许可协议 | 商用限制 |
|:----|:--------:|:--------:|
| 本技能代码（MIT） | ✅ | 无 |
| Sentence-Transformers | Apache 2.0 | 无 |
| Transformers | Apache 2.0 | 无 |
| BGE-small-zh（嵌入） | MIT | 无 |
| BGE-reranker-base（rerank） | MIT | 无 |
| 智能体推理 | — | 由运行平台提供 |

**本技能所有内置模型权重均可免费用于商业用途，无许可证冲突。**
**模型总大小约 1.2GB（bge-small 92MB + bge-reranker 1.1GB）。**
**Pipeline B 纯正则实现，零模型依赖。**
