---
name: runtime-monitor
description: AI 代理运行时 I/O 安全监控 - 检测提示注入、数据外泄、危险命令
---

# Runtime Monitor Skill

运行时 I/O 安全监控模块，保护 AI 代理免受安全威胁。

## 功能

- **提示注入检测**：识别恶意注入模式
- **数据外泄检测**：监控敏感数据传输
- **危险命令检测**：拦截高风险系统命令

## 使用场景

**使用此技能当：**
- 需要监控工具调用的输入/输出安全
- 检测潜在的安全攻击
- 审计 AI 代理行为

## 风险等级

| 等级 | 说明 |
|------|------|
| LOW | 低风险，正常操作 |
| MEDIUM | 中等风险，需关注 |
| HIGH | 高风险，建议拦截 |
| CRITICAL | 严重风险，立即阻止 |

## 集成方式

```python
from runtime_monitor import RuntimeMonitor

monitor = RuntimeMonitor()
result = monitor.detect(tool_call)
```

## 最佳实践

1. 所有外部调用前进行风险评估
2. 定期更新检测规则
3. 记录所有安全事件到审计日志
