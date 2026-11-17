> **Language**: This document is in Chinese only. For English overview, see [README.md](../README.md).
>
> **语言说明**: 本文档仅提供中文版本。英文概述请查看 [README.md](../README.md)。

---
# 结构化失败报告协议 v1.0

> 提供清晰、可操作的失败信息

---

## 报告结构

```json
{
  "status": "failed",
  "timestamp": "2026-09-10T10:30:00Z",
  "task": "任务名称",
  "error": {
    "code": "F-XXX-001",
    "message": "错误描述",
    "category": "input|generation|validation|system",
    "severity": "critical|warning|info"
  },
  "context": {
    "input": {...},
    "parameters": {...},
    "environment": {...}
  },
  "diagnosis": {
    "rootCause": "根本原因分析",
    "relatedComponents": ["组件1", "组件2"],
    "similarCases": ["案例1", "案例2"]
  },
  "solution": {
    "immediate": "立即解决方案",
    "preventive": "预防措施",
    "references": ["参考文档1", "参考文档2"]
  },
  "artifacts": {
    "generated": [...],
    "partial": [...],
    "logs": [...]
  },
  "nextSteps": [
    "步骤1",
    "步骤2"
  ]
}
```

---

## 错误分类

### Input 类错误
- F-INPUT-001: 缺少必填参数
- F-INPUT-002: 参数格式错误
- F-INPUT-003: 参数值超出范围

### Generation 类错误
- F-GEN-001: 模型调用失败
- F-GEN-002: 生成超时
- F-GEN-003: 生成结果为空

### Validation 类错误
- F-VAL-001: 输出格式验证失败
- F-VAL-002: 内容质量不达标
- F-VAL-003: 一致性检查失败

### System 类错误
- F-SYS-001: 服务不可用
- F-SYS-002: 网络错误
- F-SYS-003: 权限不足

---

## 实施检查清单

- [ ] 定义错误码体系
- [ ] 实现错误分类
- [ ] 实现诊断逻辑
- [ ] 实现解决方案生成
- [ ] 实现报告格式化

---

**版本**: v1.0  
**创建时间**: 2026-09-10
