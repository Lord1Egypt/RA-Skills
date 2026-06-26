---
name: "model-router"
description: "Intelligent model routing for OpenClaw. Automatically selects the best model from 8 available models based on task type, content length, and quality requirements."
---

# Model Router v1.0.0

智能模型路由器，为 OpenClaw 提供 8 个百炼模型的自动路由能力。

## 支持的模型

| 模型 | 上下文 | 输出 | 优势场景 |
|------|--------|------|----------|
| **qwen3.5-plus** | 1M | 65K | 通用任务、图像理解 |
| **qwen3-max** | 256K | 65K | 复杂推理、高质量输出 |
| **qwen3-coder-next** | 256K | 65K | 快速代码生成 |
| **qwen3-coder-plus** | 1M | 65K | 大型代码项目理解 |
| **MiniMax-M2.5** | 200K | 128K | 长文本生成、创作 |
| **glm-5** | 196K | 16K | 中文理解、知识问答 |
| **glm-4.7** | 196K | 16K | 快速响应、简单任务 |
| **kimi-k2.5** | 256K | 32K | 长文档、图像理解 |

## 安装

```bash
clawhub install model-router
```

## 使用方式

### 命令行

```bash
# 查询编程任务
python3 model_router.py coding quick-fix

# 查询写作任务
python3 model_router.py writing long-article 50000

# 查询分析任务
python3 model_router.py analysis complex-reasoning 0 premium
```

### Python API

```python
from model_router import ModelRouter

router = ModelRouter()

# 简单查询
model = router.select('coding', 'quick-fix')
# 返回：bailian/qwen3-coder-next

# 带参数查询
model = router.select(
    task_type='writing',
    task_subtype='long-article',
    content_length=50000,
    quality='balanced'
)
# 返回：bailian/MiniMax-M2.5

# 获取模型信息
info = router.get_model_info('bailian/qwen3.5-plus')
print(info['name'])  # 通义千问 3.5 Plus
print(info['strengths'])  # ['general', 'multimodal', 'long-context']

# 解释选择原因
explanation = router.explain_choice('bailian/MiniMax-M2.5', 'writing', 'long-article')
print(explanation)
```

## 任务类型映射

### 编程任务 (coding)
- `quick-fix` → qwen3-coder-next
- `new-feature` → qwen3-coder-plus
- `code-review` → qwen3-coder-plus
- `refactoring` → qwen3-coder-plus
- `debug` → qwen3.5-plus
- `documentation` → qwen3-coder-next
- `test` → qwen3-coder-next

### 写作任务 (writing)
- `short-content` → glm-4.7
- `long-article` → MiniMax-M2.5
- `technical-doc` → qwen3.5-plus
- `creative-writing` → MiniMax-M2.5
- `email` → glm-4.7
- `report` → qwen3.5-plus
- `script` → kimi-k2.5

### 分析任务 (analysis)
- `simple-qa` → glm-4.7
- `complex-reasoning` → qwen3-max
- `data-analysis` → qwen3.5-plus
- `research` → glm-5
- `comparison` → glm-5

### 多模态任务 (multimodal)
- `image-understanding` → qwen3.5-plus
- `document-ocr` → kimi-k2.5
- `chart-analysis` → qwen3.5-plus
- `diagram` → qwen3.5-plus

### 长上下文任务 (long-context)
- `book-summary` → qwen3-coder-plus
- `legal-doc` → qwen3.5-plus
- `meeting-notes` → MiniMax-M2.5
- `transcript` → kimi-k2.5

## 质量等级

| 等级 | 说明 | 推荐模型 |
|------|------|----------|
| **economy** | 经济快速 | glm-4.7, qwen3-coder-next |
| **balanced** | 平衡性能和成本 | qwen3.5-plus, kimi-k2.5 |
| **premium** | 最佳质量 | qwen3-max, qwen3-coder-plus |

## 配置

编辑 `/home/skyswind/.openclaw/openclaw.json`：

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "model": {
          "primary": "bailian/qwen3.5-plus",
          "fallback": ["bailian/glm-5", "bailian/kimi-k2.5"]
        }
      },
      {
        "id": "coding",
        "model": {
          "primary": "bailian/qwen3-coder-plus",
          "fallback": ["bailian/qwen3-coder-next"]
        }
      },
      {
        "id": "research",
        "model": {
          "primary": "bailian/glm-5",
          "fallback": ["bailian/qwen3-max", "bailian/qwen3.5-plus"]
        }
      },
      {
        "id": "social",
        "model": {
          "primary": "bailian/MiniMax-M2.5",
          "fallback": ["bailian/glm-4.7"]
        }
      }
    ]
  }
}
```

## 最佳实践

### 代码质量提升
- ✅ 代码审查：qwen3-coder-plus
- ✅ 新功能开发：qwen3-coder-plus
- ✅ 快速修复：qwen3-coder-next

### 写作质量提升
- ✅ 长文章：MiniMax-M2.5
- ✅ 技术文档：qwen3.5-plus
- ✅ 社交媒体：MiniMax-M2.5

### 分析质量提升
- ✅ 复杂问题：qwen3-max
- ✅ 研究报告：glm-5
- ✅ 快速问答：glm-4.7

### 成本优化
- 💰 简单任务用便宜模型（glm-4.7, qwen3-coder-next）
- 💰 复杂任务用高端模型（qwen3-max, qwen3-coder-plus）
- 💰 总体成本降低 30-50%

## 文件结构

```
model-router/
├── SKILL.md              # 技能文档
├── model_router.py       # 路由器实现
├── metadata.json         # 元数据
├── _meta.json            # 发布元数据
├── CHANGELOG.md          # 变更日志
└── references/           # 参考文档（可选）
    ├── usage-guide.md
    └── model-comparison.md
```

## 示例输出

```bash
$ python3 model_router.py coding quick-fix

推荐模型：bailian/qwen3-coder-next

🎯 选择 通义千问 Coder Next

**优势领域**: coding, quick-response
**上下文窗口**: 262,144 tokens
**最大输出**: 65,536 tokens
**速度**: fastest
**成本等级**: 💰

**适合任务**: coding → quick-fix
```

## 常见问题

### Q: 如何自定义路由规则？

编辑 `model_router.py` 中的 `TASK_MODEL_MAP` 字典。

### Q: 可以添加新模型吗？

可以，在 `MODEL_PROFILES` 中添加新模型的能力画像。

### Q: 如何追踪模型使用成本？

在 `model_router.py` 中添加日志记录，统计各模型调用次数。

## 更新日志

### v1.0.0 (2026-03-27)
- ✅ 初始版本
- ✅ 支持 8 个百炼模型
- ✅ 实现任务类型路由
- ✅ 添加命令行工具
- ✅ 添加 Python API

## License

MIT

## 作者

白龙马 🐴
