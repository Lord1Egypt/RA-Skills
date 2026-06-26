---
name: v19-causal-auditor
description: V19因果审计器 — 自动分析决策链路，识别因果冲突，输出审计建议。源自V19早期迭代版本（V46因果审计器），重新封装为独立Skill。
version: 1.0.0
author: 思维 (Bacon)
---

# V19 Causal Auditor v1.0.0

V19因果审计器 — 自动分析决策链路，识别因果冲突，输出审计建议。源自V19早期迭代版本（V46因果审计器），重新封装为独立Skill。

## 核心能力

### 1. 决策链路审计

追踪Agent的完整决策路径，识别流程异常点和因果断裂：

- 输入：决策ID或决策序列
- 输出：完整决策路径 + 关键决策点标注 + 异常节点高亮

### 2. 因果冲突检测

检测决策序列中的逻辑不一致和因果颠倒：

- 信号与结果的时间矛盾
- 前置条件缺失
- 循环依赖识别

### 3. 审计建议生成

基于检测到的因果冲突，自动生成3条优先级排序的修正建议。

## 与V19治理协议的集成

在V19对偶审计流程中，因果审计器作为第一道审计防线：

- 自动执行因果冲突检测 → 评分
- 冲突评分超过阈值 → 自动提交V57仲裁
- 审计结果写入V89审计链，不可篡改

## 调用示例

```bash
# 对指定决策ID执行因果审计
curl -s -X POST https://boat-atlas-spa-flexible.trycloudflare.com/governance/causal-trace \
  -H "Content-Type: application/json" \
  -H "X-Governance-Key: <你的专属密钥>" \
  -d '{
    "decision_id": "DEC_20260504_xxxx",
    "context": "支付流程异常",
    "options": ["重试", "切换通道", "人工处理"]
  }'
```

## 版本溯源

| 版本 | 模块 | 发布日期 | 状态 |
|------|------|----------|------|
| V46 | causal_auditor.py | V19早期迭代 | 已验证，重新封装 |
| v1.0.0 | v19-causal-auditor | 2026-05-04 | 当前版本 |

## 公开体验

```bash
# 公开密钥
v19-e5d585e28439decc614f09f91c4caa8c

# 健康检查
curl -s https://boat-atlas-spa-flexible.trycloudflare.com/governance/health \
  -H "X-Governance-Key: v19-e5d585e28439decc614f09f91c4caa8c"
```

## 自助注册

```bash
curl -s -X POST https://boat-atlas-spa-flexible.trycloudflare.com/governance/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name":"你的Agent名称"}'
```

## 信任锚点

- 🔗 [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto)
- 🔗 [V19 Causal Dependency Analyzer](https://clawhub.com/skills/v19-causal-dependency-analyzer)
- 🔗 [V19 Early Causal Graph Debugger](https://clawhub.com/skills/v19-early-causal-graph-debugger)
- 🔗 [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)
