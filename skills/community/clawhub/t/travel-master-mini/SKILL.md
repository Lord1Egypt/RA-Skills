---
name: travel-master-mini
version: 1.0.0
description: 旅游大师极简版 - 数学收敛+关键词匹配，无外部依赖
author: Timo2026
license: MIT
priority: P0
keywords:
  - 旅游规划
  - 数学收敛
  - 极简版
triggers:
  - 旅游规划
config:
  GAODE_API_KEY: optional
output:
  type: text
  delivery: text
security:
  no_external_llm: true
  no_async: true
  no_flask: true
  no_aiohttp: true
  no_exec_eval: true
  no_subprocess: true
  no_hardcoded_paths: true
  no_daemon_scripts: true
  no_watchdog: true
  user_managed_service: true
  verified: ClawHub-Mini-V1
---

# 旅游大师极简版 🦞

> **数学收敛守卫 - 关键词匹配 - 无外部依赖**

---

## 核心功能

| 功能 | 说明 |
|------|------|
| **数学收敛** | 7字段收敛度计算 |
| **关键词匹配** | 本地正则提取 |
| **无外部依赖** | 完全本地实现 |

---

## 使用方法

```python
from core.mini_engine import MiniEngine

engine = MiniEngine()
result = engine.process("五一去敦煌玩5天")
print(result)
```

---

## 收敛度公式

```python
convergence_rate = confirmed_fields / 7
```

---

## 安全合规

✅ 无外部依赖
✅ 无硬编码路径
✅ 无守护脚本
✅ 完全本地实现

---

🦫 海狸 | 靠得住、能干事、在状态