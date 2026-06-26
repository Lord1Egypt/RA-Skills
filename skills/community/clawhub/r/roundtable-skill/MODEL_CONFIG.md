# RoundTable 模型配置与自动匹配

## 📋 工作原理

### 核心原则

**RoundTable 绝不读取任何包含敏感信息的配置文件**。

所有模型信息来自：
1. ✅ OpenClaw 官方 API（优先）
2. ✅ 用户显式指定（最高优先级）
3. ✅ 标准单一模型配置（降级方案）

**绝不接触**:
- ❌ apiKey
- ❌ baseUrl
- ❌ 任何包含敏感信息的配置文件

---

## 🎯 模型获取流程

```
RoundTable 启动
      ↓
┌─────────────────────────────────┐
│ 优先级 1: 用户显式指定           │
│ - 通过参数传入模型列表          │
│ - 最高优先级，直接使用          │
└─────────────────────────────────┘
      ↓ (如果未指定)
┌─────────────────────────────────┐
│ 优先级 2: 环境变量 ROUNDTable_   │
│ - 格式："model1:tag1,tag2;      │
│          model2:tag3,tag4"      │
│ - 示例："openai/gpt-5:chinese; │
│          embedded/llama-4:     │
│          creative"              │
└─────────────────────────────────┘
      ↓ (如果未设置)
┌─────────────────────────────────┐
│ 优先级 3: OpenClaw 官方 API      │
│ - 调用 openclaw.tools API        │
│ - 获取安全的模型列表            │
│ - 已过滤敏感信息                │
└─────────────────────────────────┘
      ↓ (如果 API 不可用)
┌─────────────────────────────────┐
│ 优先级 4: 标准单一模型配置       │
│ - 降级到 anthropic/claude-4   │
│ - 所有专家都使用这个模型        │
└─────────────────────────────────┘
```

---

## 📊 使用方式

### 方式 1：自动获取（推荐）

```python
from roundtable_skill import ModelSelector

# 自动从 OpenClaw API 获取模型
selector = ModelSelector()

# 为角色匹配模型
model = selector.select_model_for_role("engineering")
# 输出：'openai/gpt-5'（假设 API 返回多个模型）
```

### 方式 2：用户显式指定

```python
from roundtable_skill import ModelSelector

# 用户显式指定可用模型列表
user_models = [
    {'id': 'openai/gpt-5', 'name': 'GLM-5', 'tags': ['chinese'], 'priority': 2},
    {'id': 'embedded/llama-4', 'name': 'Kimi K2.5', 'tags': ['creative'], 'priority': 2}
]

# 使用用户指定的模型
selector = ModelSelector(user_models=user_models)

# 为角色匹配模型
model = selector.select_model_for_role("design")
# 输出：'embedded/llama-4'（匹配 creative 标签）
```

### 方式 3：环境变量指定

```bash
# 用户通过环境变量指定
# 格式：model_id:tag1,tag2;model_id2:tag3,tag4
export ROUNDTable_MODELS="openai/gpt-5:chinese,code;embedded/llama-4:creative,long-context"

# RoundTable 自动读取环境变量
python -c "from roundtable_skill import ModelSelector; s = ModelSelector()"
# 输出：✅ 从环境变量加载 2 个模型
```

**环境变量格式说明**：
- 多个模型用分号 `;` 分隔
- 每个模型格式：`model_id:tag1,tag2,tag3`
- model_id 是完整的模型标识（如 `openai/gpt-5`）
- tags 是逗号分隔的标签列表

---

## 🔒 安全声明

### 我们读取什么

- ✅ 模型 ID（如 `anthropic/claude-4`）
- ✅ 模型名称（如 `Qwen3.5 Plus`）
- ✅ 特性标签（如 `["logic", "summary"]`）
- ✅ 优先级（如 `1`）

### 我们不读取什么

- ❌ apiKey
- ❌ baseUrl
- ❌ 任何配置文件中的敏感字段
- ❌ 用户个人数据
- ❌ 会话历史

### 审计友好

```
[审计日志]
时间：2026-03-19 18:00:00
操作：调用 openclaw.tools.get_available_models()
结果：返回模型列表（已过滤敏感信息）
风险等级：✅ 低风险
```

---

## 📝 模型匹配规则

### 角色标签定义

| 角色 | 匹配标签 |
|------|---------|
| **工程专家** | `code`, `technical`, `engineering`, `coder` |
| **体验专家** | `creative`, `long-context`, `design`, `art` |
| **测试专家** | `balanced`, `fast`, `general`, `qa` |
| **产品专家** | `chinese`, `knowledge`, `product`, `business` |
| **Host** | `logic`, `summary`, `decision`, `max` |

### 匹配算法

```python
def calculate_score(model, role_tags):
    score = 0
    
    # 标签匹配（每个标签 +10 分）
    for tag in role_tags:
        if tag in model.tags:
            score += 10
    
    # 优先级加分
    if model.priority == 1: score += 30  # 最高优先级
    elif model.priority == 2: score += 20
    else: score += 10
    
    return score
```

---

## 🎯 降级策略

### 场景 1：OpenClaw API 可用

```
可用模型：3 个
- anthropic/claude-4 (tags: logic, summary)
- embedded/llama-4 (tags: creative)
- openai/gpt-5 (tags: chinese)

匹配结果:
- 工程专家 → anthropic/claude-4 (优先级最高)
- 体验专家 → embedded/llama-4 (匹配 creative)
- 测试专家 → openai/gpt-5 (平衡型)
- Host → anthropic/claude-4 (匹配 logic)
```

### 场景 2：OpenClaw API 不可用

```
降级到标准单一模型配置
可用模型：1 个
- anthropic/claude-4 (tags: balanced, fast, general)

匹配结果:
- 工程专家 → anthropic/claude-4 (所有专家都用这个)
- 体验专家 → anthropic/claude-4
- 测试专家 → anthropic/claude-4
- Host → anthropic/claude-4
```

---

## 📋 用户配置示例

### 显式指定模型（推荐方式）

```python
# 方式 1: 通过代码指定
from roundtable_skill import run_roundtable

user_models = [
    {'id': 'openai/gpt-5', 'name': 'GLM-5', 'tags': ['chinese'], 'priority': 2},
    {'id': 'embedded/llama-4', 'name': 'Kimi K2.5', 'tags': ['creative'], 'priority': 2}
]

await run_roundtable(
    topic="智能待办应用技术方案",
    user_models=user_models  # ← 显式指定
)

# 方式 2: 通过命令行指定
ROUNDTable_MODELS="openai/gpt-5:chinese,embedded/llama-4:creative" \
  roundtable "智能待办应用技术方案"
```

### 导出/导入配置

```python
from roundtable_skill import ModelSelector

# 导出配置（用于审计和备份）
selector = ModelSelector()
selector.export_config("~/roundtable_models.json")

# 导入配置
selector = ModelSelector.import_config("~/roundtable_models.json")
```

---

## ⚠️ 注意事项

1. **不读取配置文件**: RoundTable 绝不读取 `openclaw.json` 或任何包含敏感信息的文件
2. **API 优先**: 优先使用 OpenClaw 官方 API，确保模型列表最新
3. **降级策略**: 如果 API 不可用，自动降级到标准单一模型配置
4. **用户控制**: 用户可以随时显式指定模型列表，覆盖自动获取

---

## 🔐 隐私与安全

### 设计原则

- **最小权限原则**: 只获取必要的模型元数据
- **职责分离**: 模型选择 ≠ 模型调用
- **审计友好**: 所有操作可追溯、可审计

### 数据流

```
OpenClaw API
      ↓
[模型列表] (已过滤敏感信息)
      ↓
ModelSelector
      ↓
[模型 ID]
      ↓
sessions_spawn (OpenClaw 调用)
      ↓
子 Agent 执行
```

**ModelSelector 只处理模型 ID，不接触任何敏感信息。**

---

## 📞 技术支持

- **问题反馈**: https://github.com/Krislu1221/Claw-roundtable-skill/issues
- **文档**: https://docs.openclaw.ai/skills/roundtable
- **安全审计**: 所有代码开源，欢迎审查

---

*最后更新：2026-03-19*
