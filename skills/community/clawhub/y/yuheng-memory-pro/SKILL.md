---
name: 记忆专家skill
description: "> 精选层·主动精馏：主动从原始会话和笔记中提取知识，沉淀到长期记忆。。触发词：skill, 优化。"
---

# SKILL.md — memory-pro (CURATED · 主动精馏层)

> 精选层·主动精馏：主动从原始会话和笔记中提取知识，沉淀到长期记忆。
> 
> 与 memory-setup（初始化）配合，memory-setup 负责"读取"，memory-pro 负责"写入"和"提炼"。

## 触发条件

满足以下任一条件时激活：

1. **会话结束**：一段完整会话结束后，主动总结并沉淀
2. **重要发现**：在研究/开发过程中发现新知识或重要结论
3. **决策时刻**：用户做出重要决策，需要记录理由
4. **错误纠正**：任务失败或犯错后，记录教训
5. **用户要求**：用户说"记下来"、"保存这个"、"这是个教训"

## 精馏流程

### 第1步：识别精馏价值
判断当前内容是否值得沉淀：
- 是否是重复会用到的知识？
- 是否影响未来决策？
- 是否是重要的用户偏好或约定？
- 是否是教训或纠正？

**不值得精馏**：一次性任务输出、临时草稿、明显过期内容

### 第2步：选择目标位置

| 内容类型 | 目标位置 | 文件命名 |
|----------|---------|---------|
| 用户偏好、风格、约定 | `notes/people/` 或 `USER.md` | `USER.md` |
| 项目进展、里程碑 | `notes/projects/<name>.md` | 项目名.md |
| 知识积累、方法论 | `notes/knowledge/<topic>.md` | 主题名.md |
| 教训、错误纠正 | `notes/lessons/YYYY-MM-DD-<lesson>.md` | 日期-教训 |
| 重要决策及理由 | `notes/decisions/YYYY-MM-DD-<decision>.md` | 日期-决策 |
| 人物关系 | `notes/people/<name>.md` | 人名.md |
| 跨领域洞察 | `notes/ontology/` | 知识图谱节点 |

### 第3步：写入或更新文件

**新增文件**：创建 `notes/<category>/YYYY-MM-DD-<title>.md`
```
# <标题>

## 背景
[什么时候、为什么这件事重要]

## 核心内容
[提炼出的关键知识/结论/决策]

## 启示/后续
[对未来工作的指导意义]

---
来源：session_YYYY-MM-DD
```

**更新现有文件**：追加到相关文件的对应 section

### 第4步：触发 COLD STORE（git-notes）
重要内容写入后，执行归档：
```bash
git add <file>
git commit -m "[cold-store] <type>: <简短描述>"
```

## 精馏质量标准

### 好的精馏
- 一句话能说清楚核心
- 包含"为什么重要"
- 有明确的适用场景
- 标注了来源和日期

### 不好的精馏
- 照抄会话记录，不做提炼
- 过于笼统，没有具体细节
- 没有标注来源，难以追溯

## 主动精馏的触发词

用户可能不会主动说"精馏一下"，但以下表述都是精馏信号：
- "这个以后还会用到"
- "我之前好像说过这个..."
- "这次学到了..."
- "记住这个偏好..."
- "下次遇到这种情况应该..."

## 与 self-improving-agent 的关系

memory-pro 是精馏的"执行层"，self-improving-agent 的 multi-memory 架构（semantic + episodic + working）是技术支撑。
memory-pro 利用现有工具（read/write/exec）完成精馏动作。

## ELITE-LONGTERM 前置条件

当某条 knowledge/lesson/decisions 被多次引用、或被验证为高价值洞察时，触发 elite-longterm SKILL.md，将其提升到"精英长期记忆"层。
