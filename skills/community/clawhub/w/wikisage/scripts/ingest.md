# Ingest 流程

当用户提供文档、PDF、URL，或产生了有价值的回答时执行。

所有 wiki 读写走 Obsidian MCP（详见 SKILL.md 执行通道）。
简写下方示例省略了 `--config`，实际调用要带上：
`--config $MCPORTER_CONFIG`（默认 `~/.openclaw/workspace/config/mcporter.json`）

示例里的 `$WIKI_ROOT` 默认是 `~/.openclaw/workspace/wiki`，`$WIKI_SKILL_DIR` 默认是 `~/.openclaw/workspace/skills/wikisage`。

---

## ⚠️ 强制：Step 0 去重检查（来源是文件/URL 时必跑）

如果 ingest 来源是 **具体文件或 URL**（PDF、博文、文档链接），**读之前**先算 SHA256 去重：

```bash
python3 $WIKI_SKILL_DIR/scripts/dedup.py check <file_or_url>
```

- 输出 `NEW` → 继续下面的 Step 1
- 输出 `DUPLICATE` → **停下**，告诉用户这个内容已 ingest 过（并指出对应 wiki 页面），问是否强制重新入库

如果来源是 **用户对话内容或即兴结论**（没有原始文件/URL），**跳过 Step 0**，直接从 Step 1 开始。

写完页面后，在最后的 Step 4/5 之间加一步记录缓存：
```bash
python3 $WIKI_SKILL_DIR/scripts/dedup.py \
  record <file_or_url> pages/<category>/<slug>.md "来源标题"
```

---

## ⚠️ 强制：先判断，再决定怎么存

### Step 1：读 index.md，找相关页面

```bash
mcporter call obsidian.read_text_file path=$WIKI_ROOT/index.md
```

扫描所有已有页面标题和描述，判断新内容与哪个页面最相关。

### Step 2：判断存法

```
新内容
  │
  ├── index.md 里有相关页面？
  │     │
  │     ├── YES：内容是什么类型？
  │     │     ├── 扩展/补充现有概念 → 更新现有页面，追加新章节
  │     │     ├── 独立子主题（可单独成篇）→ 新建页面 + 原页面加 [[链接]]
  │     │     ├── 与现有内容矛盾 → 标注矛盾，询问用户哪个正确
  │     │     └── 完全重复 → 不存，告知用户已有相关内容
  │     │
  │     └── NO → 新建页面
  │
  └── 存完后：更新 index.md（页面数 + 1，加条目）
```

### Step 3：判断标准详细说明

| 情况 | 判断依据 | 做法 |
|------|---------|------|
| 同一概念的不同角度 | 主题词相同（如都是"NIS 2"）| 更新现有页面 |
| 独立子主题 | 标题不同，但有交叉（如"NIS 2 行动清单"vs"NIS 2 概述"）| 新建 + 交叉链接 |
| 完全不同的主题 | 无重叠 | 新建页面 |
| 内容矛盾 | 两处对同一事实描述不同 | 询问用户 |

---

## 标准 Ingest 流程

```
Step 0: 去重检查（dedup.py check，只对文件/URL 类来源）
         - NEW    → 继续
         - DUPLICATE → 停下并告知用户已 ingest 过
Step 1: 读 index.md（MCP read_text_file，判断是否已有相关页面）
Step 2: 根据判断：
         - 新建 → MCP write_file（整篇）
         - 更新 → MCP edit_file（局部）或 write_file（整篇覆盖）
Step 3: 追加 wiki/log.md（MCP edit_file，append-only，格式：## [YYYY-MM-DD] ingest | 标题）
Step 4: 更新 wiki/index.md（MCP edit_file：新建加条目；更新改描述）
Step 4.5: 记录去重缓存（dedup.py record，只对文件/URL 类来源）
Step 5: 一次 ingest 可能触碰 5-15 个相关页面，逐一更新交叉引用（MCP edit_file）
Step 6: 告知用户存储结果（页面路径 + 更新了哪些页面）
```

### MCP 调用示例

```bash
# 新建页面
mcporter call obsidian.write_file \
  path=$WIKI_ROOT/pages/aws/security-hub.md \
  content='# Security Hub

**最后更新：** 2026-04-25
...'

# 更新页面（局部改）
mcporter call obsidian.edit_file \
  path=$WIKI_ROOT/pages/aws/security-hub.md \
  edits='[{"oldText":"## 相关页面\n- [[A]]","newText":"## 相关页面\n- [[A]]\n- [[B]]"}]'

# 追加 log.md（用 edit_file 在文件尾部加一行；或整篇读+写）
```

---

## 页面文件命名规范

```
$WIKI_ROOT/pages/
├── aws/              AWS 服务、合规、架构
│   └── sources/      原始文档摘要（raw sources）
├── ai/               AI/LLM 相关
│   └── sources/
├── projects/         项目相关
└── ops/              运维相关
```

- 文件名：小写 + 连字符，如 `security-hub.md`、`nis2-compliance-checklist.md`
- sources/ 下存原始文档摘要，父目录下存编译后的知识页面

---

## 页面模板

```markdown
# 页面标题

**最后更新：** YYYY-MM-DD
**来源数量：** N
**分类：** aws/security（路径）
**置信度：** EXTRACTED  <!-- EXTRACTED | INFERRED | AMBIGUOUS | UNVERIFIED -->

## 概述
一段话说清楚这个主题是什么。

## 核心内容
...

<!-- 段落级置信度 inline tag（混合置信度的页面必须打）： -->
<!-- [EXTRACTED] 原文直接扒的 -->
<!-- [INFERRED]  基于来源推理 -->
<!-- [AMBIGUOUS] 来源本身模糊 -->
<!-- [UNVERIFIED] AI 自己补的常识，没来源 -->

## 相关页面
- [[相关页面名]]

## 来源
- [[原始文档页面名]]
- [外部链接](https://...)
```

**置信度标注原则：**
1. frontmatter 的 `置信度:` 是整页默认值，**不要省**
2. 页面里如果一部分是来源原文扒的（EXTRACTED）、一部分是 AI 推断的（INFERRED），**必须在段落前加 inline tag**
3. Query 时引用 INFERRED/UNVERIFIED 的内容，回答里要明说是推断的
4. 详细规则见 SKILL.md「置信度标签规则」

---

## Ingest 完成后的轻量 lint

```bash
python3 $WIKI_SKILL_DIR/scripts/lint.py --quick
```

只查 index.md 一致性，防止 ingest 留脏。
