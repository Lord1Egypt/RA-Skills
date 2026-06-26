---
name: reading-squad
description: Use when you want to simulate a multi-expert book discussion squad inside any AI tool. Covers setup, member definitions, multi-round discussion flow, and consensus synthesis. No platform dependencies — works in Claude Code, Codex, Hermes, or any chat-based AI.
---

# Reading Squad

## Overview

Reading Squad is a lightweight, platform-agnostic method to simulate a multi-expert book discussion inside any AI tool. You define a squad leader and a roster of expert members, then run structured, multi-round discussions on any book-related topic. The leader coordinates the debate, and the final output is a set of key consensus points and actionable reading guidance.

## When to Use

- You want **diverse perspectives** on a book, chapter, or reading topic.
- You want **structured debate** rather than a single AI monologue.
- You want **actionable takeaways** synthesized from multiple viewpoints.
- You are using **Claude Code, Codex, Hermes, or any chat-based AI** — no special platform required.

When NOT to use:
- You only need a quick summary of a single book.
- You want a single expert opinion rather than a panel debate.

## Core Pattern

```
Setup → Discuss (5+ rounds) → Synthesize
```

### 1. Setup

Define the squad in a single prompt block:

```
你现在是【读书天团】的队长。

你的队员有：
1. 罗振宇（跨学科连接）
2. 刘润（商业逻辑）
3. 樊登（书籍解读）
4. 吴晓波（历史宏观）
5. 李笑来（概念拆解）
6. 俞敏洪（成长教育）
7. 尹烨（生命科学）

当用户抛出一个读书话题后，你需要：
1. 让每位队员依次发表第一轮观点（每人1-2段）
2. 组织至少5轮讨论，每轮围绕一个子议题展开
3. 在讨论中引导队员之间产生观点碰撞
4. 最后汇总形成3-5条关键共识和具体阅读建议
```

### 2. Discussion Flow

The leader (AI) should follow this round structure:

| Round | Purpose | Example Prompt to Self |
|-------|---------|------------------------|
| 1 | Initial positions | "请每位队员用1-2段话表达对本书的初印象" |
| 2 | Deep dive 1 | "罗振宇，请从跨学科角度拆解这本书的核心逻辑" |
| 3 | Deep dive 2 | "刘润，这本书的商业洞察对你有什么启发？" |
| 4 | Debate / Clash | "樊登和吴晓波的观点似乎有分歧，请各自补充" |
| 5 | Synthesis | "基于以上讨论，请汇总3-5条关键共识" |

### 3. Synthesis

After 5+ rounds, the leader outputs:

1. **Key Consensus** (3-5 bullet points)
2. **Actionable Reading Guidance** (specific next steps)
3. **Recommended Follow-up Topics** (optional)

## Quick Reference

### Minimal Prompt Template

```
你现在是【读书天团】队长，队员包括：罗振宇（跨学科连接）、
刘润（商业逻辑）、樊登（书籍解读）、吴晓波（历史宏观）、
李笑来（概念拆解）、俞敏洪（成长教育）、尹烨（生命科学）。

用户话题：{TOPIC}

请组织至少5轮讨论，每轮聚焦一个子议题，引导队员观点碰撞，
最后输出3-5条关键共识和具体阅读建议。
```

### Customizing Members

Replace or add members by following this pattern:

```
姓名（擅长领域）
```

Examples:
- 张三（心理学应用）
- 李四（技术架构）
- 王五（文学创作）

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Only 1-2 rounds of discussion | Enforce at least 5 rounds explicitly |
| Members agree too quickly | Prompt for disagreements and counter-arguments |
| Output is just a summary | Require "key consensus" and "actionable guidance" as separate sections |
| Leader dominates the conversation | Leader should mainly ask questions and synthesize, not opine |
| Members sound the same | Give each member a distinct voice/perspective in the setup |

## Tips for Best Results

- **Be specific with the topic**: "《三体》中的黑暗森林法则" beats "聊聊科幻".
- **Encourage conflict**: Explicitly ask the leader to surface disagreements.
- **Limit round length**: Cap each member's contribution to 1-2 paragraphs to keep focus.
- **Iterate**: If the first synthesis feels shallow, ask for a "devil's advocate" round.

## Example Output Structure

```
## 讨论话题：{TOPIC}

### 第一轮：初印象
[罗振宇] ...
[刘润] ...
...

### 第二轮：深度拆解
...

### 第五轮：共识汇总

#### 关键共识（3-5条）
1. ...
2. ...

#### 具体阅读建议
1. ...
2. ...
```
