---
name: uniskill-v4
version: 4.1.0
description: 极简AI Agent框架 - 3%解决方案。从8771行精简到1000行，保留苏格拉底探明+多模型辩论核心方法论。
author: Timo2026
license: MIT
tags:
  - ai-agent
  - socratic-engine
  - multi-model-debate
  - minimalist
---

# UniSkill V4 - 极简AI Agent框架

**3%解决方案：8,771行 → 1,000行**

## 触发条件

**自动触发**：
- 用户说 "帮我评估"、"验证这个"、"哪个更好"、"点子王验证"
- 涉及开源/闭源策略决策
- CNC报价相关（材料、加工、零件）
- 多方案选择问题

## 使用方式

```python
from core_v4 import process_with_uniskill_v4

result = process_with_uniskill_v4(user_input)
if result.triggered:
    if result.needs_more_info:
        return result.question  # 苏格拉底追问
    else:
        return result.recommendation  # 辩论推荐
```

# UniSkill V4 - 极简AI Agent框架

**3%解决方案：8,771行 → 260行**

## 核心模块

### 1. 苏格拉底引擎 (60行)
- 5W2H需求锚定
- 收敛系数判断 (0.7阈值)
- 只在关键参数缺失时"咬人"

### 2. 高速辩论器 (80行)
- 异步多模型对抗
- 商业分析师/技术顾问/投资顾问
- 五维评分体系

### 3. 编排器 (120行)
- 整合探明+辩论
- 内存安全 (<100MB)
- 超时保护

## 快速开始

```python
from uniskill_v4 import check_clarity, quick_debate

# 检查需求清晰度
is_clear, prompt = check_clarity("帮我加工10个TC4零件")

# 多模型辩论
result = quick_debate(
    "开源框架还是开源应用？",
    ["开源框架，闭源应用", "全部开源", "全部闭源"]
)
```

## 设计哲学

### 保留的（V2精华）
- ✅ 苏格拉底需求探明
- ✅ 多模型对抗辩论
- ✅ 收敛系数阈值
- ✅ 五维评分体系

### 剔除的（V2冗余）
- ❌ 独立收敛检查器
- ❌ 复杂提问模板
- ❌ 伪造日志
- ❌ 24个冗余模块

## 性能对比

| 版本 | 代码量 | 模块数 | 启动时间 |
|------|--------|--------|----------|
| V2 | 8,771行 | 27个 | ~5秒 |
| **V4** | **260行** | **3个** | **<0.5秒** |

## 作者

**Timo** - miscdd@163.com  
**海狸 (Beaver)** - 靠得住、能干事、在状态

## 许可证

MIT License

---

**靠得住、能干事、在状态** 🦫
---

> 所有文件均由大帅教练系统生成/dashuai coach
