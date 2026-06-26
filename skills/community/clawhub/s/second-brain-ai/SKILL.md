---
name: second-brain-ai
version: 2.3.3
description: Read, capture, search, relate, and assemble context from a user-specified local Markdown knowledge base (Obsidian/Logseq style). Supports controlled write operations with explicit approval and attribution. Use when the user wants a Second Brain / note-vault memory layer for Markdown notes, including saving ideas, searching past notes, finding related notes or backlinks, building context packs, appending to existing notes (with attribution), or getting smart link suggestions.
---

# Second Brain AI Skill v2.0 (Repair Build)

A lightweight skill for working with a user-chosen Markdown knowledge base with controlled write operations and attribution requirements.

## Requirements

- Node.js >= 16.0.0
- Environment variable `SECOND_BRAIN_VAULT` must be set explicitly
- Optional: Frontmatter support (YAML)
- Optional: WikiLinks support `[[Note Title]]`

## Configuration

```bash
export SECOND_BRAIN_VAULT="/absolute/path/to/your/vault"
```

## Safety Boundaries

- Only operates within the configured vault path
- Write operations require `allow_write: true`
- Append operations require `appended_by` attribution
- Do not assume a private vault path. Use `SECOND_BRAIN_VAULT` or ask the user for the configured vault.
- Do not turn raw transcripts into permanent notes without summarizing, attributing, and asking for write approval.

## Human-Brain Handshake Workflow

When the user is building long-term knowledge, optimize for a clean handoff between the agent and the user's 人脑.

1. **Recall before write**
   - Run `search_notes`, `find_related`, or `build_context_pack` before creating durable notes, unless the user explicitly asks for a quick capture.
   - Summarize what already exists and name the gap the new note fills.
2. **Evidence and attribution**
   - Label content as user-provided, agent-synthesized, imported, or inferred.
   - Keep source snippets short and attach note titles or paths when available.
   - Mark unresolved questions instead of smoothing them into false certainty.
3. **Write gate**
   - Ask for explicit approval before `capture_note`, `append_note`, or `init_vault`.
   - Require `allow_write: true` and a meaningful `appended_by` value for append operations.
   - Before appending, check for likely duplicate notes or conflicting claims.
4. **Context-pack output**
   - Provide relevant notes, strongest snippets, open questions, suggested links, and a recommended next thinking step.
   - Do not claim semantic search, vector indexing, or automatic conflict resolution; this repair build is file-scan based.

Preferred response shape:

```text
Recall: <existing notes or none found>
Gap: <what is missing or newly clarified>
Proposed write: <new note or append target>
Approval needed: <yes/no + why>
Next thinking step: <one question for the user's 人脑>
```

## Tools

### 1. init_vault
Initialize a new vault with standard folder structure.

**Input:** `{ "allow_write": true }`

### 2. capture_note
Create a new note.

**Input:**
```json
{
  "allow_write": true,
  "title": "Note Title",
  "content": "Body content",
  "type": "idea",
  "tags": ["tag1", "tag2"],
  "links": ["Related Note"]
}
```

### 3. append_note
Append content to an existing note with attribution.

**Input:**
```json
{
  "allow_write": true,
  "title": "Note Title",
  "content": "Additional content",
  "section": "Updates",
  "appended_by": "Agent Name"
}
```

**Required:** `appended_by` must identify who is appending.

### 4. search_notes
Search notes by keywords.

**Input:** `{ "query": "search terms", "limit": 5 }`

### 5. find_related
Find notes related to a topic.

**Input:** `{ "topic": "Topic Name", "limit": 5 }`

### 6. get_backlinks
Get notes that link to a specific note.

**Input:** `{ "note_title": "Target Note" }`

### 7. build_context_pack
Build a context pack for agent consumption.

**Input:** `{ "topic": "Topic", "limit": 10 }`

### 8. suggest_links
Get smart link suggestions for a note.

**Input:** `{ "title": "Note Title", "limit": 5 }`

### 9. rebuild_index
Refresh index (currently returns skip status as SQLite is not implemented).

**Input:** `{}`

## Note Format

Standard frontmatter:
```yaml
---
id: 20260313
title: Note Title
type: idea
tags: [tag1, tag2]
created: 2026-03-13
updated: 2026-03-13
status: active
---
```

## Append Attribution Format

When appending, the skill adds:
```markdown
> Append Record
> Added by: {appended_by}
> Added at: {timestamp}

{content}
```

## Limitations (Repair Build)

- SQLite indexing is not implemented; uses file-based scanning
- No semantic/vector search
- No automatic link insertion
- No conflict detection
- Single vault only

## Testing

```bash
npm test
```

---

## 🚀 First-Success Path

**30秒快速上手：三步开始使用第二大脑**

1. **设置知识库路径** — 配置 `SECOND_BRAIN_VAULT` 环境变量指向你的 Obsidian/Logseq 笔记文件夹
2. **快速记录一条笔记** — 使用 `capture_note` 输入标题和内容，如"阅读《思考快与慢》笔记"
3. **搜索已有笔记** — 使用 `search_notes` 查找相关内容，验证笔记已成功建立

> 示例：`capture_note` → 标题 "今日灵感" → 内容 "关于AI Agent的记忆管理新思路" → `search_notes` 搜索"Agent 记忆"确认收录

---

## 📝 Sample Prompts

### 示例 1：快速记录新想法
**用户输入：**
```
帮我记一个想法：今天开会提到可以用知识图谱来优化推荐系统的冷启动问题。标签用「推荐系统」「知识图谱」。
```

**期望输出：**
```
✅ 笔记已创建

📝 推荐系统冷启动思路
─────────────────
标题: 推荐系统冷启动-知识图谱方案
类型: idea
标签: #推荐系统 #知识图谱
内容: 今天开会提到可以用知识图谱来优化推荐系统的冷启动问题。

你可以：
- `search_notes` 搜索"冷启动"查看相关笔记
- `find_related` 查找"推荐系统"相关内容
- `suggest_links` 获取关联建议链接
```

### 示例 2：搜索笔记内容
**用户输入：**
```
搜索一下我关于"注意力机制"的笔记
```

**期望输出：**
```
🔍 找到 5 条相关笔记

1️⃣ Transformer中的注意力机制详解
   路径: vault/AI/transformer-attention.md
   标签: #深度学习 #NLP #Transformer
   片段: "Self-Attention 的核心是QKV..."

2️⃣ 注意力机制与人类认知的类比
   路径: vault/思考/attention-cognition.md
   标签: #认知科学 #注意力
   片段: "人类注意力也是资源有限的..."

3️⃣ 推荐系统中的注意力池化
   路径: vault/推荐系统/attention-pooling.md
   标签: #推荐系统 #深度学习

📎 `find_related topic:"注意力机制"` 查看更多关联笔记
```

### 示例 3：查找相关笔记
**用户输入：**
```
帮我找找和「强化学习」有关的笔记
```

**期望输出：**
```
🔗 与「强化学习」相关的 5 条笔记

1️⃣ Policy Gradient 算法笔记
   关联度: ★★★★★
   标签: #强化学习 #深度学习

2️⃣ 马尔可夫决策过程基础
   关联度: ★★★★☆
   标签: #强化学习 #数学

3️⃣ AlphaGo 的技术演进
   关联度: ★★★☆☆
   标签: #AI #强化学习 #博弈

4️⃣ RLHF 在LLM中的应用
   关联度: ★★★★☆
   标签: #强化学习 #LLM

5️⃣ 多臂老虎机与推荐系统
   关联度: ★★★☆☆
   标签: #推荐系统 #强化学习

📎 需要构建上下文包？ → `build_context_pack topic:"强化学习"`
```

### 示例 4：构建上下文包
**用户输入：**
```
帮我整理一份关于「知识蒸馏」的上下文包，给我看 demo 和写文档用
```

**期望输出：**
```
📦 上下文包：知识蒸馏（10条笔记）

┌─ 知识蒸馏笔记（20XX-XX-XX）
├─ 蒸馏温度参数调优（20XX-XX-XX）
├─ Student-Teacher 框架（20XX-XX-XX）
├─ 蒸馏在BERT中的应用（20XX-XX-XX）
├─ 离线蒸馏 vs 在线蒸馏（20XX-XX-XX）
├─ 知识蒸馏的损失函数（20XX-XX-XX）
├─ KD 与剪枝/量化的对比（20XX-XX-XX）
├─ 知识蒸馏在推荐系统的实践（20XX-XX-XX）
├─ 蒸馏的 3 篇必读论文（20XX-XX-XX）
└─ 我的学习总结（20XX-XX-XX）

→ 已打包为 agent 上下文，可直接使用
```

### 示例 5：追加笔记内容
**用户输入：**
```
刚才那条"Transformer中的注意力机制详解"笔记，帮我追加一段最近看的关于Flash Attention的内容，标注是「金豆追加」
```

**期望输出：**
```
✅ 已追加内容

📝 Transformer中的注意力机制详解
─────────────────────
更新部分（由 金豆追加 于 2026-06-16）：

> Flash Attention 的关键改进：
> 1. 分块计算避免全局 O(n²) 内存占用
> 2. 利用 GPU 共享内存减少显存读写
> 3. 支持更长的序列长度

笔记现在共含 2 条更新记录。可查看 `Updates` 部分阅读完整内容。
```

---

## 📋 Real Task Examples

| 场景 | 用户输入示例 | 技能输出要点 |
|------|-------------|-------------|
| **快速记录** | "刚想到一个做项目的思路，帮我记下来" | 创建新笔记 → 自动提取关键信息 → 生成合理标签 → 确认保存位置 |
| **检索知识库** | "我之前记过关于Docker部署的笔记吗？" | 关键词搜索 → 高亮匹配内容 → 展示笔记路径/标签 → 建议相关查询 |
| **关联发现** | "我最近在研究RAG，帮我找找和这相关的所有笔记" | 多维度关联搜索 → 匹配度排序 → 呈现知识网络 → 建议下一步阅读 |
| **上下文准备** | "明天要给团队讲微服务架构，帮我整理相关笔记" | 构建上下文包 → 按日期/主题组织 → 提取关键段落 → 可做演示素材 |
| **知识更新** | "那篇关于React Hooks的笔记，补充一下useEffect的新改动" | 定位目标笔记 → 追加内容并标注来源 → 保留修改历史 → 确认更新完成 |
