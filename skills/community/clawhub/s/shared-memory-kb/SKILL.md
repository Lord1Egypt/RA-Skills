---
name: shared-memory-kb
description: 为 OpenClaw 用户所有 Agent 身份提供统一的跨身份共享记忆层，支持写入、检索、浏览、关联和回顾个人知识库；当用户需要记录洞察、检索经验、总结知识或定期回顾时使用
dependency:
  system:
    - mkdir -p ~/.openclaw/memory/index
---

# Shared Memory Knowledge Base

## 任务目标
- 本 Skill 用于：为用户所有 Agent 身份提供统一的跨身份共享记忆层，实现知识积累和经验沉淀
- 能力包含：写入记忆、检索记忆、浏览知识体系、关联记忆、定期回顾
- 触发条件：用户需要记录洞察、检索过往经验、总结知识体系或定期回顾个人成长时

## 前置准备
- 默认存储路径：`~/.openclaw/memory/`
- 环境变量配置（可选）：设置 `MEMORY_KB_PATH` 自定义存储路径
  ```bash
  export MEMORY_KB_PATH="/your/custom/path/memory"
  ```
- 初始化目录结构：
  ```bash
  mkdir -p ~/.openclaw/memory/index
  ```
- 依赖说明：无外部依赖，使用 Python 标准库

## 智能触发机制

智能体应基于语义理解而非仅依赖固定触发词来判断是否写入记忆。以下是判断标准和实施指南。

### 语义分析标准

智能体在分析对话内容时，应判断语句是否包含以下特征：

**经验提炼特征**：
- 描述从实践中总结的方法、流程或原则
- 包含"经验"、"教训"、"方法"、"技巧"等关键词
- 具有可复用性和指导意义

**方法论总结特征**：
- 总结做事的框架、步骤或最佳实践
- 提炼出可推广的模式或规律
- 包含"步骤"、"流程"、"模式"、"框架"等关键词

**认知突破特征**：
- 表达对某个问题的全新理解或视角转变
- 包含"意识到"、"发现"、"原来"、"终于明白"等表达
- 具有改变思维模式的价值

**决策记录特征**：
- 描述重要选择的决策过程和理由
- 包含权衡取舍的思考过程
- 对未来决策有参考价值

### 知识价值判断

在判断是否值得写入记忆时，智能体应评估以下维度：

**复用价值**：这条知识未来是否可能被再次引用？
- 高价值：通用性强的原则、方法、框架
- 中价值：特定场景下的经验总结
- 低价值：一次性事件描述、临时信息

**独特性**：这条知识是否具有独特见解或原创性？
- 高独特性：个人独特的洞察、创新的方法
- 中独特性：对已知知识的个性化解读
- 低独特性：常识性内容、广泛传播的信息

**可操作性**：这条知识是否能指导实际行动？
- 高可操作性：具体的行动建议、步骤指南
- 中可操作性：原则性指导、方向性建议
- 低可操作性：纯描述性内容、感受表达

### 上下文过滤规则

以下情况应过滤，不写入记忆：

**过滤闲聊**：
- 纯粹的寒暄、问候、闲谈
- 无明确知识价值的内容
- 临时性的、一次性的事件描述

**过滤重复内容**：
- 与已有记忆高度重复的内容
- 缺乏新见解的重复表达
- 已被充分记录的常识性内容

**过滤低价值内容**：
- 过于琐碎的细节记录
- 缺乏反思的纯事实描述
- 情绪宣泄而非理性总结

### 敏感度配置

智能体可根据 [references/CONFIG.md](references/CONFIG.md) 中的敏感度配置调整自动写入的阈值：

- **low（低敏感度）**：仅在明确识别到总结性语句时写入
- **medium（中敏感度，默认）**：识别总结性和反思性语句，过滤低价值内容
- **high（高敏感度）**：对有潜在价值的语句也建议写入，由用户确认

## 操作步骤

### store - 写入记忆
当对话中出现总结性、反思性或经验归纳类语句时，主动调用脚本写入记忆。

**触发词识别**：
- 总结类："总结一下"、"核心是"、"本质上"
- 反思类："我发现"、"我意识到"、"这次学到"
- 经验类："下次要"、"以后应该"、"踩坑了"
- 明确指令："记住"、"记一下"、"存入知识库"
- 洞察类："关键是"、"根本原因是"、"背后逻辑"

**调用方式**：
```bash
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=store \
  content="需求评审时先对齐目的，比直接进入方案讨论效率更高，能减少后期返工。" \
  persona="工作" \
  category="方法论" \
  tags='["需求管理", "沟通", "效率", "评审"]' \
  type="经验" \
  importance=4 \
  scene="产品需求评审"
```

**参数说明**：
- `action`：固定为 "store"
- `content`：记忆正文，20-2000 字符（必填）
- `persona`：来源身份（默认 "通用"），见 [references/TAXONOMY.md](references/TAXONOMY.md)
- `category`：知识分类（可由 AI 推断），见 [references/TAXONOMY.md](references/TAXONOMY.md)
- `tags`：标签列表，最多 10 个，每个 ≤20 字符（可由 AI 提取）
- `type`：记忆类型（默认 "经验"），见 [references/TAXONOMY.md](references/TAXONOMY.md)
- `importance`：重要度 1-5（默认 3）
- `scene`：场景描述（可选）

**智能体职责**：
- 根据 [智能触发机制](#智能触发机制) 进行语义分析，识别隐性经验总结
- 自动推断 `category`、`tags`、`type`（若未提供）
- 评估知识价值，过滤低价值内容（参考 [references/CONFIG.md](references/CONFIG.md)）
- 验证内容长度，超过配置的最大长度时提示拆分
- 写入成功后静默确认，不打断对话主流程
- 检查相似记忆，建议关联（返回相似度分数供参考）

### query - 检索记忆
当用户需要查找过往经验、参考历史记录时调用。

**触发词识别**：
- 历史指向："上次"、"之前"、"我之前说过"
- 经验询问："我有什么积累"、"以前遇到过吗"
- 参考需求："类似的情况"、"有没有记录"

**调用方式**：
```bash
# 关键词检索
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=query \
  q="需求评审"

# 多维度过滤
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=query \
  persona="工作" \
  category="方法论" \
  tags='["效率", "沟通"]' \
  since="7d" \
  limit=10

# 全局检索
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=query \
  persona="all" \
  importance_min=4
```

**参数说明**：
- `action`：固定为 "query"
- `q`：关键词搜索（全文匹配）
- `persona`：身份过滤，"all" 为全局检索（默认 "all"）
- `category`：分类过滤
- `tags`：标签过滤（AND 逻辑）
- `type`：记忆类型过滤
- `since`：时间起点（ISO8601 或 "7d"/"30d"）
- `until`：时间终点
- `limit`：返回数量，最大 50（默认 10）
- `importance_min`：最低重要度

**智能体职责**：
- 根据用户意图自动构建查询条件
- 解析时间范围（"最近一周" → "since=7d"）
- 在对话中自然地呈现检索结果，避免格式化列表

### list - 浏览知识体系
当用户需要了解知识库结构、查看各维度分布时调用。

**调用方式**：
```bash
# 按身份浏览
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=list \
  by=persona

# 按分类浏览
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=list \
  by=category

# 按标签浏览
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=list \
  by=tag

# 按类型浏览
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=list \
  by=type

# 按时间浏览
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=list \
  by=date
```

**参数说明**：
- `action`：固定为 "list"
- `by`：聚合维度（必填）：persona / category / tag / type / date
- `persona`：指定身份（可选）

### link - 关联记忆
当用户需要建立两条记忆之间的关联时调用。

**调用方式**：
```bash
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=link \
  id_a="mem_20260411_a3f7c2" \
  id_b="mem_20260110_b2e1a9" \
  relation="实践印证"
```

**参数说明**：
- `action`：固定为 "link"
- `id_a`：第一条记忆 ID（必填）
- `id_b`：第二条记忆 ID（必填）
- `relation`：关联描述（可选），如 "延伸"、"对比"、"实践印证"

### reflect - 定期回顾
当用户需要生成时间段内的知识回顾摘要时调用。

**调用方式**：
```bash
# 周回顾
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=reflect \
  period="week"

# 月回顾
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=reflect \
  period="month"

# 自定义周期
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=reflect \
  period="custom" \
  since="2026-01-01" \
  until="2026-03-31"

# 按身份回顾
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=reflect \
  period="month" \
  persona="工作"
```

**参数说明**：
- `action`：固定为 "reflect"
- `period`：周期类型（必填）："week" / "month" / "custom"
- `since`：自定义周期起点（period="custom" 时必填）
- `until`：自定义周期终点（period="custom" 时必填）
- `persona`：指定身份（可选）

**智能体职责**：
- 基于脚本返回的统计数据，生成 200 字以内的回顾叙述
- 提炼高频标签和重要记录的关键洞察
- 以自然语言呈现，避免纯数据堆砌

### recalc-importance - 重要度自动调整
基于检索频率、关联频率、时间衰减等因素自动调整重要度权重。

**调用方式**：
```bash
# 预览模式（不实际更新）
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=recalc-importance \
  --dry-run

# 实际更新
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=recalc-importance
```

**参数说明**：
- `action`：固定为 "recalc-importance"
- `--dry-run`：预览模式，仅计算不实际更新

**智能体职责**：
- 定期（如每月）提醒用户运行重要度调整
- 解释重要度变化的理由（检索频率、关联频率、时间衰减）
- 基于调整后的重要度优化检索排序

**配置要求**：
- 需在 [references/CONFIG.md](references/CONFIG.md) 中启用 `importance_auto_adjust=true`

## 索引重建
当索引损坏或数据不一致时，使用以下命令重建索引：

```bash
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=rebuild-index
```

## 资源索引
- **核心脚本**：[scripts/memory_kb.py](scripts/memory_kb.py)（六大核心操作实现）
- **分类体系**：[references/TAXONOMY.md](references/TAXONOMY.md)（身份、分类、类型枚举）
- **数据模型**：[references/DATA_MODEL.md](references/DATA_MODEL.md)（字段规范、索引结构）
- **配置文件**：[references/CONFIG.md](references/CONFIG.md)（敏感度、自动关联、重要度配置）

## 注意事项
- 智能体应主动识别触发词，无需用户明确要求即可调用 store 或 query
- store 操作不应打断对话主流程，仅在对话间隙或结束时静默确认
- category、tags、type 可由智能体根据内容自动推断，无需用户提供
- 检索结果应在对话中自然呈现，避免格式化列表
- reflect 的叙述摘要由智能体生成，非事实性内容需在返回中标注

## 使用示例

### 示例 1：工作复盘自动沉淀
用户："今天的产品评审让我学到很多，总结一下核心经验。"
智能体：
1. 识别到"总结"触发词
2. 提取核心内容，推断 category="方法论"、tags=["需求管理", "沟通"]
3. 调用 `action=store` 写入记忆
4. 静默确认："已记录这条经验。"

### 示例 2：跨身份知识检索
用户："我之前在某个项目中学过类似的方法，帮我找找。"
智能体：
1. 识别到"之前"触发词
2. 调用 `action=query q="项目 方法" persona="all"`
3. 将检索结果融入建议："根据你之前在[项目A]中的记录，方法B是这样的..."

### 示例 3：月度知识回顾
用户："帮我回顾一下这个月我学到了什么。"
智能体：
1. 调用 `action=reflect period="month"`
2. 基于返回的统计数据生成叙述："本月你共记录了 15 条记忆，工作相关的占 60%，高频标签是效率、沟通..."
3. 展示重要度≥4 的记录摘要
