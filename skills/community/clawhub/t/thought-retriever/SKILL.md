# Thought-Retriever Skill

> 将每次对话中生成的回答，提炼成可积累、可复用的"知识晶体"，驱动AI记忆系统的自我进化。

## 核心原理

Thought-Retriever 脱胎于论文 arXiv:2604.12231，其核心洞察是：

**不要只检索原始数据，要检索 LLM 生成的想法（Thoughts）。**

每次对话后，LLM的回答中蕴含着有价值的洞察——这些洞察才是记忆系统的核心养料，而不是原始对话日志。

## 五步循环

```
用户问题
    ↓
步骤1: 检索相关 Thought
    ↓（从 ontology 中找最相关的已有 Thought）
步骤2: 生成回答
    ↓（由主模型完成，这里只记录结果）
步骤3: 提炼候选思想 + 计算置信度
    ↓（用 LLM 从回答中抽取知识晶体，赋置信度）
步骤4: 查重剔除冗余
    ↓（相似度 > θ → 合并；置信度 < γ → 丢弃）
步骤5: 更新记忆
    ↓（新增/合并 Thought 到 ontology）
```

## 阈值参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| γ（gamma） | 0.6 | 置信度阈值，低于此值的新 Thought 直接丢弃 |
| θ（theta） | 0.80 | 相似度阈值，高于此值视为重复，合并已有 |

## 存储结构

每个 Thought 是 ontology 中的一个实体：

```json
{
  "id": "thou_59a993f9",
  "type": "Thought",
  "properties": {
    "content": "AI接单系统可以通过结合微信群与竞标平台形成多渠道互补",
    "confidence": 0.8,
    "last_accessed": "2026-05-02T07:42:59+00:00",
    "source": "conversation",
    "query": "赵匡的AI接单系统包括哪些渠道"
  }
}
```

## 置信度评分标准

| 分数 | 含义 |
|------|------|
| 0.9-1.0 | 明确验证过的结论，多个证据支持 |
| 0.7-0.8 | 合理推断，有一定依据 |
| 0.5-0.6 | 初步观察，可能需要验证 |
| <0.5 | 丢弃 |

## 文件位置

```
~/.openclaw/workspace/skills/thought-retriever/
  thought_retriever.py   ← 核心引擎
  SKILL.md              ← 本文件

~/.openclaw/workspace/memory/ontology/
  graph.jsonl           ← Thought 实体存储
  schema.yaml           ← Thought 类型定义
```

## 使用方式

### 命令行调用

```bash
python skills/thought-retriever/thought_retriever.py \
  --query "用户问题" \
  --answer "生成的回答" \
  --feedback "用户反馈（可选）"
```

### 配置为对话后钩子（OpenClaw）

在 OpenClaw 配置中注册为 post-turn 钩子，每次对话结束自动触发。

### 手动运行测试

```bash
python skills/thought-retriever/thought_retriever.py \
  --query "赵匡的AI接单系统包括哪些渠道" \
  --answer "包括微信群接单和dealwork.ai平台竞标两个渠道"
```

## 与其他组件的关系

| 组件 | 作用 |
|------|------|
| **ontology** | 提供存储和检索 Thought 的基础设施 |
| **self-improving** | 记录失败案例，影响新 Thought 的初始置信度 |
| **Evolver** | 读取 Thoughts，作为自我进化的分析素材 |

## 注意事项

- 使用百炼 glm-5.1 模型（不走代理）
- 每个 Thought 都有 `query` 字段，记录生成它时的原始问题
- 置信度会在后续相关查询被触发时自动提升
- 定期检查 `memory/ontology/graph.jsonl` 中的 Thought 数量和置信度分布
