---
when: 想看完整前后走查、某步骤拿不准（尤其 Gate 0 判定 / 五类预标 / description 1-minimal）
topics: walkthrough, good-vs-bad, retirement, routing-signal, faithfulness, anti-pattern
---

# 走查 1：通过案例 — `skill-hotword-extractor`

## 输入 idea
> "做一个从会议纪要提取领域热词的 skill"

## Step 0: Retirement check

3 个典型触发场景：

- "帮我提取这段会议文字的热词"
- "这段文字的关键术语是什么"
- "帮我识别这次客户会议的行业词"

**裸模型测试**：Claude 直接回能给出关键词，但**不会按"最小化拆分 / 不放错公司 / 不保留通用词"的领域规则**——这三条规则才是 skill 的独特价值。Gate 0 **通过**。

## Step 1: 三要素

- primary capability（15 tok）：从非结构化文本提取领域热词
- trigger condition（12 tok）：用户粘会议文字 / 通话记录要关键词时
- unique identifier（10 tok）：hotword / 最小化拆分 / 行业术语

## Step 2: Description（约 45 tok）

> "从会议 / 通话文本提取领域热词，遵循最小化拆分 / 不保留通用词 / 不放错公司三条规则。用户粘记录要关键词时触发。"

**DDMIN 自检**：删"从会议 / 通话" → 泛化过度（和通用关键词工具混淆），保留。

## Step 3: Body 预标

| 规则 / 内容 | 分类 | 去向 |
|-----------|------|------|
| 输出 JSON Array：`{term, category, confidence}` | `template` | `SKILL.md`（短，合回） |
| category 枚举：`{product, company, tech, jargon}` | `core_rule` | `SKILL.md` |
| 最小化拆分：`iPhone 15 Pro` → `iPhone`，不拆到 `Pro` | `core_rule` | `SKILL.md` |
| 不保留通用词（`产品` / `会议` / `讨论`） | `core_rule` | `SKILL.md` |
| 不放错公司名（提到"苹果"不等于 `Apple Inc.`） | `core_rule` | `SKILL.md` |
| 为什么最小化拆分：避免长尾 noise | `background` | `background.md` |
| 输入 `下个月要上 iPhone 15` → 输出 `[{term: iPhone, ...}]` | `example` | `examples.md` |

## Step 4: File split

- `SKILL.md`（≈180 tok）：3 条 core_rule + category 枚举 + JSON 格式（template 合回，因短）
- `background.md`（≈60 tok）：最小化拆分的动机
- `examples.md`（≈120 tok）：3–5 个 I/O 对

## Step 5: 四反模式

- examples-as-specification？ ✓ 规则全在 core_rule，示例只是风格示范
- background 藏阈值？ ✓ 无数字
- description 堆触发词？ ✓ 45 tok 无枚举
- redundant？ ✓ refs 未重复

## Step 6: Faithfulness（Gate 1）

operational concept：`JSON Array`, `term/category/confidence`, `{product,company,tech,jargon}`, `最小化拆分`, `不保留通用词`, `不放错公司` → 全在 `core_rule` ∪ `template`。**通过**。

---

# 走查 2：退休案例 — `skill-json-prettifier`

## 输入 idea
> "做一个格式化 JSON 的 skill"

## Step 0: Retirement check

3 个场景：
- "帮我格式化这段 JSON"
- "pretty-print 一下"
- "缩进一下"

**裸模型 / 现有工具测试**：
- Claude 直接能做 ✓
- `jq .` 或 `python -m json.tool` 能做 ✓
- 没有领域规则 / 独特价值 ✓

**Gate 0 建议退休**。反馈用户：

> "这个用裸 Claude 或 `jq` 都可以，建 skill 反而增加 router 负担和维护成本。论文 10.7% skill 属于此类，建议不做。"

**不进入 Step 1**。

---

# 走查 3：description 1-minimal 过程

**初稿**（过泛，8 tok）：
> "一个帮助用户的 skill"
>
> router 无法唯一匹中任何查询 → 扩充。

**+primary capability**（12 tok）：
> "从 PDF 提取表格数据的 skill"
>
> 还能被"PDF 转文字"等无关查询误匹 → 加 trigger。

**+trigger condition**（20 tok）：
> "从 PDF 提取表格数据。用户粘 PDF 路径要表格时触发。"
>
> 和"其他 PDF 工具"还会撞 → 加 unique identifier。

**+unique identifier**（36 tok）：
> "从 PDF 提取表格数据，输出 Markdown 表。用户粘 PDF 路径要表格时触发。工具：pdfplumber + tabula-py。"

最后一版可被"帮我提 PDF 表"和"pdfplumber" 两类查询唯一匹中。**DDMIN 验证**：删"工具：pdfplumber..." → "pdfplumber" 查询 miss，保留。

---

# 常见预标错误

## examples-as-specification 陷阱

看似 example，其实藏 rule：

> "响应格式：
> Q: How do I deploy?
> A: Run `make deploy` in the `staging/` directory, check `/var/log/app.log`"

**错分**：整段 → `example`
**问题**：`make deploy`、`staging/`、`/var/log/app.log` 会在 Faithfulness 丢失
**正确**：
- `make deploy`, `staging/`, `/var/log/app.log` → `core_rule`
- Q&A 风格 → `example`

## background 藏阈值

> "因为 pipeline 对延迟敏感，所以 timeout 用 500ms 而不是默认 30s"

**错分**：整段 → `background`
**问题**：`500ms` 是操作阈值
**正确**：
- "timeout 500ms" → `core_rule`
- "为什么 500ms" → `background`（可选）

## Redundant 误判

body 最后一段：
> "See `references/api-spec.md` for the full API specification."

**错分**：`core_rule`（看起来是指令）
**正确**：`redundant`。这是 progressive disclosure 的路由提示，应由拆出文件的 `when:` / `topics:` metadata 替代，原段丢弃。
