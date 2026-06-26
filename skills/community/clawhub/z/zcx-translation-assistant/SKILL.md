---
name: translation-assistant
description: Professional multilingual translation with domain-specific terminology handling for finance, law, and technology. Use when the user needs to: (1) translate content between Chinese and English (or other language pairs), (2) preserve formatting in Markdown, tables, code blocks, or structured documents, (3) produce bilingual (side-by-side) output for comparison, (4) ensure technical/legal/financial term consistency, (5) check translation quality or standards compliance. Primary supported pair: zh-CN ↔ en. Additional pairs on request.
emoji: 🌐
---

# Translation Assistant — 多语言翻译助手

Professional, domain-aware translation between Chinese (Simplified) and English, with optional side-by-side bilingual output and format preservation.

## Supported Language Pairs

| Pair | Direction | Proficiency |
|:-----|:----------|:------------|
| zh-CN ↔ en | 双向 | ⭐⭐⭐⭐⭐ 母语级 |
| zh-TW ↔ en | 双向 | ⭐⭐⭐⭐ |
| zh-CN ↔ ja | 双向 | ⭐⭐⭐ |
| zh-CN ↔ ko | 双向 | ⭐⭐⭐ |
| en ↔ fr/de/es | 双向 | ⭐⭐⭐⭐ |

**Default:** Chinese (Simplified) ↔ English. Other pairs require explicit user request.

## Supported Domain Glossaries

| Domain | Key Terminology | Example |
|:-------|:----------------|:--------|
| **Finance / 金融** | 期货(futures), 期权(options), 保证金(margin), 结算价(settlement price), 做多/做空(long/short), 持仓量(open interest), 交割(delivery), 套保(hedge) | 原油期货主力合约 → front-month crude oil futures contract |
| **Legal / 法律** | 甲方(Party A), 乙方(Party B), 不可抗力(force majeure), 保密(confidentiality), 管辖(governing law), 违约(breach of contract) | 终止协议 → termination agreement |
| **Technology / 科技** | API, 微服务(microservices), 部署(deploy), 容器化(containerization), 持续集成(CI), 负载均衡(load balancing), 数据库(database/DB) | 灰度发布 → canary release |
| **Medical / 医药** | 临床试验(clinical trial), 适应症(indication), 不良反应(adverse event), 剂量(dosage) | 双盲随机对照试验 → double-blind randomized controlled trial |

## How to Translate

### Step 1: Determine translation parameters

Ask the user (or infer from context):

1. **Source and target languages**
   - Default: zh-CN → en for business/tech, en → zh-CN for learning
   - Reverse or other: confirm explicitly

2. **Domain**
   - General / 通用 (default)
   - Finance / 金融 — Use glossary terms (保证金 → margin, not "deposit")
   - Legal / 法律 — Preserve legal precision, keep Latin terms (force majeure, mutatis mutandis)
   - Technology / 科技 — Keep English technical terms if more common in industry
   - Medical / 医药 — Use exact medical terminology

3. **Output format**
   - **Direct translation** — Only target language, natural flow
   - **Bilingual (side-by-side)** — Original + translation, paragraph-level alignment:

     ```markdown
     **原文**: [original text]
     **译文**: [translated text]
     ```
   - **Bilingual (interlinear)** — Sentence by sentence:

     ```markdown
     [Original sentence 1]
     [Translation sentence 1]

     [Original sentence 2]
     [Translation sentence 2]
     ```
   - **Format-preserving** — Keep all Markdown, tables, code blocks, lists, headings intact (replace only text content)

### Step 2: Classify text & apply rules

#### General / 通用翻译
- Prioritize natural readability
- Adjust sentence structure: Chinese topic-comment → English subject-verb-object
- Handle culturally specific references: 身在曹营心在汉 → "to appear loyal while secretly working against"

#### Finance / 金融翻译
| 中文 | English (Correct) | ✗ Avoid |
|:-----|:------------------|:---------|
| 期货合约 | futures contract | future contract (singular) |
| 开仓 | open a position | open position (ambiguous) |
| 平仓 | close a position | close position |
| 爆仓 | forced liquidation / margin call | explode warehouse ✗ |
| 浮盈/浮亏 | unrealized P&L | floating gain/loss |
| 交割日 | delivery date / expiry | — |
| 集运欧线 | container shipping (Europe route) / EC | — |
| 期现套利 | cash-and-carry arbitrage | — |

#### Legal / 法律翻译
- Preserve sentence structure — legal language is precise
- Official names: 中华人民共和国XXX法 → XXX Law of the People's Republic of China
- Keep standard legal boilerplate terms:
  - 本协议 → this Agreement (capitalized)
  - 一方 → a Party / either Party
  - 包括但不限于 → including but not limited to
  - 自生效之日起 → as of the Effective Date
  - 具有法律约束力 → legally binding

#### Technology / 科技翻译
- Keep proper nouns in original English (AWS, GitHub, Kubernetes, React)
- Translate verbs and concepts, keep API names/tokens unchanged
- Code blocks: **never translate** code content, only comments and strings

```python
# BAD (translated code)
def 获取数据():  # ✗ Don't translate function names
    返回 "你好"

# GOOD (translate comments only)
def fetch_data():  # 获取数据
    return "hello"
```

### Step 3: Check format preservation

For each element type:

| Element | Action |
|:--------|:-------|
| **Title / Heading** | Translate heading text, keep heading level |
| **Bold / Italic** | Keep formatting markers, translate content inside |
| **Link [text](url)** | Translate display text, keep URL unchanged |
| **Image ![](alt)** | Translate alt text, keep URL |
| **Code block** | Translate comments/strings only, keep code syntax untouched |
| **Table** | Translate cell content, keep column count and alignment |
| **List** | Translate item content, keep list structure (ordered/unordered) |
| **Blockquote** | Translate quoted text, keep > markers |
| **Separator ---** | Keep as-is |

### Step 4: Output the translation

Follow the format the user requested (or default to bilingual side-by-side for accuracy-sensitive content, direct translation for readability).

### Step 5: Optional quality check

If the user requested a quality review or if the content is complex:

1. **Readability** — Does the translation read naturally in the target language?
2. **Terminology consistency** — Same term translated the same way throughout?
3. **Numeric accuracy** — Numbers, dates, amounts match exactly
4. **Omission check** — No content skipped
5. **Hallucination check** — No content added that wasn't in the original

Report any findings.

## Special Cases

### Markdown-heavy content (README, docs, wiki pages)
Always use **format-preserving** mode. Keep all Markdown structure, translate inline text only.

### Financial statements / tables
Preserve all numeric values. Translate headers, footnotes, and metadata. Keep row/column structure identical.

### Contracts and legal documents
Always use **bilingual output**. Translate every clause line by line. Preserve numbering and section structure. Flag ambiguous terms with `[待确认]`.

### Very long documents (>10,000 words)
Summarize the structure first, translate section by section, and offer to compile into a single output file.

### Code comments and docstrings
Translate comment text, keep variable/function/class names, keep `@param` and `@return`/`Args:`/`Returns:` structure tags.

## Reference: Common False Friends

| Chinese Term | Common Wrong | Correct |
|:-------------|:-------------|:--------|
| 精密 | precision (mechanical) | high-precision |
| 敏感词 | sensitive word | censorship keyword / banned term |
| 干货 | dry goods | valuable content / substance |
| 痛点 | pain dot | pain point |
| 上线 | online | go live / launch / deploy |
| 下班 | off work | get off work / leave for the day |
| 你懂的 | you know | you know what I mean (rely on context) |
| 洪荒之力 | prehistoric power | with all one's might / give it one's all |

## Special Notes

- **Accuracy over fluency** — When in doubt, a slightly awkward but accurate translation is better than a fluent but wrong one
- **For business/formal contexts**, use neutral, professional tone. For casual or marketing content, adjust tone naturally
- **Preserve all inline code** — `variable_names`, `functionCalls()`, CSS classes, URLs, file paths — leave completely unchanged
- **When translating API documentation**, keep every command, code sample, and JSON structure intact
- **If the user provides only a file path**, read the file, translate, and write a new file with `_translated` or language suffix appended to the filename
- **Document length**: For each major output section, pause and ask the user to continue if the total translation output is expected to be very long
