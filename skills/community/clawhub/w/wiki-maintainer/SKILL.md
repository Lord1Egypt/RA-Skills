# SKILL.md — wiki-maintainer

> 维护 llm-wiki 知识库的标准操作程序。

**适用场景：** 用户要求 ingest 来源、提问、从 wiki 中查找信息、执行 lint 检查。

**目标 wiki：** `/Users/clax/Documents/doc_synced/llm-wiki/`

---

## 读取引擎

每次操作前，读取目标 wiki 的 `AGENTS.md` 和 `index.md` 了解当前状态。

---

## 操作一：Ingest（新来源）

当用户提供了新的文档/文章/笔记，需要纳入知识库时：

### Step 1 — 判断来源类型

- **纯文本内容**（直接粘贴的文字）：存入 `raw/sources/<slug>.md`
- **网络文章**：用 jina fetch 抓取，存入 `raw/sources/<slug>.md`
- **文件路径**：复制到 `raw/` 对应子目录

### Step 2 — 生成摘要页

根据 `AGENTS.md` 的 Source 摘要页模板，写 `wiki/sources/<slug>.md`：
- 提取核心观点（3-5 条）
- 记录关键细节/引述
- 标注与现有 wiki 内容的关联
- 列出待探索问题

### Step 3 — 更新 Entity / Concept 页面

扫描摘要中出现的具名实体和概念：
- 已存在 → 追加新信息，更新 `updated` 日期
- 不存在 → 按模板新建页面

### Step 4 — 必要时创建 Synthesis

如果新来源涉及跨多个已有页面的主题：
- 新建或更新 `wiki/syntheses/<topic>.md`
- 标注矛盾点、共识点

### Step 5 — 更新 index.md

- 在对应类别添加新条目
- 更新 `更新时间`
- 更新计数

### Step 6 — 记录 log.md

```markdown
## [YYYY-MM-DD HH:MM] ingest | <来源标题>
<简要描述：新增了哪些页面，有什么重要发现>
```

### Step 7 — 向用户汇报

```
✅ Ingest 完成：<来源标题>
📄 新建摘要：wiki/sources/<slug>.md
🔗 关联实体：entity/xxx, entity/yyy
💡 值得关注：<1-2 个亮点>
```

---

## 操作二：Query（提问）

当用户向 wiki 提问时：

### Step 1 — 读 index.md

找到与问题相关的页面列表。

### Step 2 — 读取相关页面

读取最相关的 3-5 个 wiki 页面（entities/concepts/sources）。

### Step 3 — 回答

综合 wiki 内容生成答案，适当使用 `[[wiki/...]]` 链接。

### Step 4 — 可选：存回 wiki

如果答案有价值（系统性分析、对比、新发现），生成 `wiki/builds/<slug>.md`：
- 标题为问题本身
- 内容为答案
- 附上来源依据

### Step 5 — 记录 log.md

```markdown
## [YYYY-MM-DD HH:MM] query | <问题摘要>
<简要描述答案亮点>
```

---

## 操作三：Lint（健康检查）

当用户要求检查 wiki 健康状态，或每累积 10 次 ingest 后自动触发：

### Step 1 — 运行工具

```bash
bash /Users/clax/Documents/doc_synced/llm-wiki/tools/lint.sh
```

### Step 2 — 读取结果并修复

常见问题及处理：
- **orphan pages**：添加引用或在 index.md 标注"待关联"
- **来源未同步**：立即 ingest 缺失的来源
- **frontmatter 缺失**：补充完整
- **index 过期**：重新生成 index.md

### Step 3 — 报告

向用户报告检查结果和修复动作。

---

## 操作四：Batch Ingest（批量导入）

当 `raw/` 中有多个待处理来源时：

1. 逐个处理（不要并行），每处理完一个汇报一个
2. 最后做一次整体 lint
3. 统一更新 index.md

---

## 页面模板速查

```
wiki/sources/<slug>.md   → Source 摘要页模板
wiki/entities/<name>.md  → Entity 实体页模板
wiki/concepts/<name>.md  → Concept 概念页模板
wiki/syntheses/<topic>.md → Synthesis 综合页模板
wiki/builds/<slug>.md     → Build 产出页模板
```

详见 AGENTS.md 完整规范。

---

## 注意事项

- **永远不修改 raw/ 中的文件**（来源不可变）
- wiki 内容由 LLM 全权维护，人类不直接编辑
- 回答时优先读 wiki，而非重新从网络搜索（wiki 中已有编译好的知识）
- 发现矛盾时，在相关页面标注"⚠️ 存疑"并记录具体矛盾点

---

_Last updated: 2026-04-12_
