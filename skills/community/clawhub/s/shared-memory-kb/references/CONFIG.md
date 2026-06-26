# Configuration - 配置文件

## 目录
- [配置概述](#配置概述)
- [敏感度配置](#敏感度配置)
- [存储配置](#存储配置)
- [自动关联配置](#自动关联配置)
- [重要度配置](#重要度配置)
- [配置文件管理](#配置文件管理)

---

## 配置概述

Shared Memory Knowledge Base 支持通过配置文件自定义行为。配置文件位于 `~/.openclaw/memory/config.json`，如果不存在则使用默认值。

**默认配置示例**：

```json
{
  "auto_write_sensitivity": "medium",
  "min_content_length": 20,
  "max_content_length": 2000,
  "max_tags_count": 10,
  "max_tag_length": 20,
  "auto_link_threshold": 0.5,
  "importance_auto_adjust": true,
  "importance_recalc_days": 30
}
```

---

## 敏感度配置

### auto_write_sensitivity

控制智能体自动写入记忆的敏感度。

**可选值**：
- `low`：低敏感度，仅在明确识别到总结性语句时写入
- `medium`：中敏感度（默认），识别总结性和反思性语句，过滤低价值内容
- `high`：高敏感度，对有潜在价值的语句也建议写入，由用户确认

**使用建议**：
- 初期使用 `medium`，观察知识库质量
- 如果发现过多低价值内容，调整为 `low`
- 如果担心遗漏重要知识，调整为 `high`

**智能体行为差异**：

| 敏感度 | 写入条件 | 过滤规则 |
|-------|---------|---------|
| low | 明确的总结词（总结、经验、方法等） | 过滤所有低价值内容 |
| medium | 总结词 + 反思性语句 + 认知突破 | 过滤闲聊、重复、低价值内容 |
| high | 任何有潜在价值的语句 | 仅过滤纯闲聊 |

---

## 存储配置

### min_content_length

写入记忆的最小内容长度。

**默认值**：20 字符
**范围**：10-100 字符
**说明**：过短的内容通常不具备知识价值

### max_content_length

写入记忆的最大内容长度。

**默认值**：2000 字符
**范围**：1000-5000 字符
**说明**：超过此长度的内容应拆分为多条记忆

### max_tags_count

单条记忆允许的最大标签数量。

**默认值**：10
**范围**：5-20
**说明**：过多标签会影响检索效率

### max_tag_length

单个标签的最大长度。

**默认值**：20 字符
**范围**：10-50 字符
**说明**：标签应简洁，避免过长的描述

---

## 自动关联配置

### auto_link_threshold

自动关联记忆的相似度阈值。

**默认值**：0.5
**范围**：0.0-1.0
**说明**：
- 0.0：不进行自动关联
- 0.5：中等相似度（标签匹配 + 内容关键词重叠）
- 0.7：高相似度（严格的标签匹配）
- 1.0：完全匹配（仅完全相同的标签）

**相似度计算公式**：
```
相似度 = (标签匹配分数 × 0.6) + (内容关键词重叠分数 × 0.4)
```

**使用建议**：
- 初期使用 `0.5`，观察关联质量
- 如果关联过多无关内容，调高阈值
- 如果关联过少，调低阈值

---

## 重要度配置

### importance_auto_adjust

是否启用重要度自动调整功能。

**默认值**：`true`
**可选值**：`true` / `false`

**启用后行为**：
- 系统会根据检索频率、关联频率、时间衰减自动调整重要度
- 高频检索的记忆重要度会逐渐提升
- 长期未检索的记忆重要度会逐渐降低
- 调整周期由 `importance_recalc_days` 控制

### importance_recalc_days

重要度自动调整的计算周期。

**默认值**：30 天
**范围**：7-90 天
**说明**：每隔此天数执行一次重要度重新计算

**重要度调整算法**：

```
新重要度 = 基础重要度 + 检索频率加成 + 关联频率加成 - 时间衰减

其中：
- 基础重要度 = 原始设定的 importance
- 检索频率加成 = min(检索次数 × 0.5, 2.0)
- 关联频率加成 = 关联次数 × 0.3
- 时间衰减 = (当前时间 - 创建时间) / 365 × 0.5

最终重要度限制在 1-5 范围内
```

---

## 配置文件管理

### 创建配置文件

如果不存在配置文件，系统会使用默认值。创建自定义配置：

```bash
cat > ~/.openclaw/memory/config.json << EOF
{
  "auto_write_sensitivity": "high",
  "max_content_length": 3000,
  "auto_link_threshold": 0.6
}
EOF
```

### 验证配置

使用以下命令验证配置是否有效：

```bash
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=validate-config
```

### 重置为默认值

删除配置文件即可恢复默认值：

```bash
rm ~/.openclaw/memory/config.json
```

### 配置热更新

配置文件修改后立即生效，无需重启。

---

## 配置最佳实践

### 1. 敏感度渐进式调整

建议从 `medium` 开始，根据实际效果逐步调整：

```bash
# 第1个月：medium（观察）
"auto_write_sensitivity": "medium"

# 第2个月：如遗漏较多 → high
"auto_write_sensitivity": "high"

# 第3个月：如冗余较多 → low
"auto_write_sensitivity": "low"
```

### 2. 标签数量与质量平衡

根据知识库规模调整标签限制：

```json
// 小型知识库（< 100条）：允许更多标签
"max_tags_count": 15

// 中型知识库（100-1000条）：标准配置
"max_tags_count": 10

// 大型知识库（> 1000条）：严格控制标签
"max_tags_count": 8
```

### 3. 自动关联阈值优化

根据关联质量调整：

```bash
# 阶段1：宽松（建立初步关联网络）
"auto_link_threshold": 0.4

# 阶段2：收紧（提升关联质量）
"auto_link_threshold": 0.6

# 阶段3：精细（仅保留强关联）
"auto_link_threshold": 0.7
```

### 4. 重要度自动调整监控

启用重要度自动调整后，定期回顾：

```bash
# 每月查看重要度变化
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=recalc-importance \
  --dry-run
```

`--dry-run` 参数表示仅计算不实际更新，便于预览变化。

---

## 配置示例

### 保守型配置（适合初学者）

```json
{
  "auto_write_sensitivity": "low",
  "max_content_length": 2000,
  "max_tags_count": 5,
  "auto_link_threshold": 0.7,
  "importance_auto_adjust": false
}
```

### 平衡型配置（推荐）

```json
{
  "auto_write_sensitivity": "medium",
  "max_content_length": 2000,
  "max_tags_count": 10,
  "auto_link_threshold": 0.5,
  "importance_auto_adjust": true,
  "importance_recalc_days": 30
}
```

### 激进型配置（适合重度用户）

```json
{
  "auto_write_sensitivity": "high",
  "max_content_length": 3000,
  "max_tags_count": 15,
  "auto_link_threshold": 0.4,
  "importance_auto_adjust": true,
  "importance_recalc_days": 7
}
```
