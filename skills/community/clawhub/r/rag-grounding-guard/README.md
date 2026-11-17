# rag-grounding-guard · RAG事实溯源校验 / RAG Grounding Guard

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

RAG dies not on "no retrieval" but on "retrieved yet unused, plus fabricated". Verify each claim against retrieved sources: coverage rate + uncovered claims flagged as hallucination risk; citations must carry a source (registered). Runnable `grounding_check.py`. Theoretical root: LGD — registered (citation) + evidenced (verifiable).

### Why it beats "trust the retrieved docs"

| Pain | This skill |
|---|---|
| Model fabricates beyond sources | Per-claim coverage check |
| Citation points nowhere | Citations must carry source |
| No quality metric | Grounding coverage rate (evidenced) |

### What's inside

- `SKILL.md` — 2 checks + 3-step flow + iron rule
- `scripts/grounding_check.py` — zero-dependency CLI: claim-vs-source coverage

```bash
python scripts/grounding_check.py --claims claims.txt --sources sources.txt
```

### Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Vector rerank | Better top-k | No claim-level grounding |
| "It cited a doc" | Vague | Citation may be wrong doc |
| Human spot-check | Slow | Not per-claim, not scaled |

Theoretical root: **LGD Three Laws** — registered + evidenced. Pairs with `context-engineering`.

## 中文

逐条校验声明是否被检索来源支撑，未覆盖标红为幻觉风险，引用强制带出处。附可运行脚本（`grounding_check.py`）。理论根基：LGD 有籍（引用溯源）+ 有证（可核验）。

### 为什么比「信检索到的文档就行」强

| 痛点 | 本技能 |
|---|---|
| 模型编出来源外的东西 | 逐声明覆盖校验 |
| 引用指了个寂寞 | 引用必须带出处 |
| 没有质量指标 | grounding 覆盖率（有证） |

### 里面有什么

- `SKILL.md` — 两查 + 三步流程 + 铁律
- `scripts/grounding_check.py` — 零依赖 CLI：声明 vs 来源覆盖比对

```bash
python scripts/grounding_check.py --claims claims.txt --sources sources.txt
```

### 与同类对比

| 工具 | 它做什么 | 本技能补的缺口 |
|---|---|---|
| 向量重排 | top-k 更好 | 无声明级 grounding |
| "它引了篇文档" | 含糊 | 可能引错文档 |
| 人工抽查 | 慢 | 不逐声明、不可规模化 |

理论根基：**LGD 三律**——有籍 + 有证。与 `context-engineering` 配套。

---

© 2026 SynomosAI. All rights reserved.

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
