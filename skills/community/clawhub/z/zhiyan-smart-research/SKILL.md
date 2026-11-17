---
name: zhiyan-smart-research
slug: zhiyan-smart-research
version: 1.1.0
description: 智研学术探索 v1.1 — 一问即出结构化报告：结论摘要、文献综述、空白与创新、研究建议、追问方向。Crossref/PubMed + OpenClaw LLM. Use for literature search, review, research gaps, 文献检索, 学术探索.
homepage: https://clawhub.ai/skills/zhiyan-smart-research
metadata: {"openclaw":{"emoji":"🔬","requires":{"bins":["python3"]},"os":["darwin","linux"]}}
---

# Smart Research · 智研学术探索 v1.1

**提问即检索，结论必溯源** — 用户提一个问题 → 检索文献 → 输出**结构化研究报告**。

| 组件 | 职责 |
|------|------|
| **本 Skill** | Crossref + PubMed 检索 |
| **OpenClaw LLM** | 按 v1.1 模板撰写各章节 |
| **OpenClaw 记忆** | 会话上下文 + `research/sessions/` |

## v1.1 标准流程（每次必走）

```
用户问题
  → search_literature.py（英文检索词）
  → LLM 按模板写报告（6 个章节）
  → save_research.py 存档
  → 向用户展示完整报告
```

### Step 1 — 检索

根据用户问题提炼 **英文检索词**，执行：

```bash
python3 {baseDir}/scripts/search_literature.py "<english query>" > /tmp/papers.json
```

检索词建议：核心概念 + `review` / `research gap` / `recent` 等（按意图选择）。

### Step 2 — 撰写报告（Agent + OpenClaw LLM）

读取 `/tmp/papers.json` 的 `papers` 数组，`[n]` = 第 n 篇。

**必须输出以下 6 节（顺序固定）：**

| 章节 | 要求 |
|------|------|
| **结论摘要** | 3–5 句；概括核心发现；每句带 `[n]` |
| **参考文献** | 表格：序号、标题、作者、年份、来源、链接 |
| **文献综述** | 约 **300 字**；梳理脉络、方法、共识；关键句带 `[n]` |
| **研究空白与创新点** | 条目列出；基于文献，无依据标「待验证」 |
| **研究建议** | 约 **200 字**；2–3 条可执行方向 |
| **追问建议** | **恰好 3 条**具体追问方向 |

完整模板见：[templates/report-template.md](templates/report-template.md)

**写作规则：**
- 仅依据检索到的 papers；不得编造 DOI、作者、数据
- 无文献支撑的判断写「待进一步检索验证」
- 中文输出；专有名词可保留英文

### Step 3 — 存档

将完整报告写入临时文件后保存：

```bash
python3 {baseDir}/scripts/save_research.py \
  --topic "<用户原问题>" \
  --report-file /tmp/report.md \
  --papers-json /tmp/papers.json
```

或分字段传入：

```bash
python3 {baseDir}/scripts/save_research.py \
  --topic "..." \
  --summary "结论摘要…" \
  --review "文献综述…" \
  --gaps "空白与创新…" \
  --recommendations "研究建议…" \
  --follow-ups $'方向1\n方向2\n方向3' \
  --papers-json /tmp/papers.json
```

### Step 4 — 追问

用户选择「追问建议」中某一方向时：

1. 读 `{baseDir}/research/sessions/<id>.md`
2. 针对新方向再检索（可选）
3. **重新输出完整 v1.1 六节报告**（非片段回复）
4. `--session-id <id>` 更新存档

## 输出示例（结构）

```markdown
## 结论摘要
该领域近五年在…方面进展显著 [1][2]。… [3]

## 参考文献
| 序号 | 标题 | 作者 | 年份 | 来源 | 链接 |
| [1] | … | … | 2024 | crossref | https://doi.org/… |

## 文献综述
（约300字）

## 研究空白与创新点
- **空白 1**：… [4]
- **创新点 1**：…

## 研究建议
（约200字）

## 追问建议
1. …
2. …
3. …
```

## 何时使用

- 用户提出学术/科研问题，需要**一次性结构化报告**
- 文献检索、综述、空白分析、创新点挖掘
- 关键词：文献检索、学术探索、智研、research gap、literature review

## 环境变量（可选）

| 变量 | 说明 |
|------|------|
| `CROSSREF_MAILTO` | Crossref 联系邮箱 |

## 故障排查

| 现象 | 处理 |
|------|------|
| 某节缺失 | 对照模板补全六节后再回复用户 |
| 综述字数不足 | 扩展文献综述至约 300 字 |
| 追问建议 ≠ 3 条 | 必须恰好 3 条 |

## 参考

- [templates/report-template.md](templates/report-template.md)
- [examples.md](examples.md)
- [USAGE.md](USAGE.md)
