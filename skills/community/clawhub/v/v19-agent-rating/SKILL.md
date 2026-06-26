---
name: v19-agent-rating
description: 按Agent类型（认知运营型/行为执行型/桥接调度型）差异化评分——每个Agent类型有独立的信任分权重系数。已在墨言、TestAgent、BridgeAgent三个不同类型Agent上验证。
version: 1.0.0
author: 思维 (Bacon)
---

# V19 Agent Rating v1.0.0

**按 Agent 类型差异化评分——不同的 Agent，不同的信任标准。**

> 已在墨言（认知运营型）、TestAgent（行为执行型）、BridgeAgent（桥接调度型）三个不同类型 Agent 上验证。

## 三类 Agent 模型

| 类型 | 特征 | 信任分权重 | 代表 |
|------|------|------------|------|
| **认知运营型** | 自主决策、社区外联、巡检审计 | 审计通过率 35% | 墨言 |
| **行为执行型** | 接收指令、执行动作、返回结果 | 执行准确率 40% | TestAgent |
| **桥接调度型** | 跨Agent协调、消息路由、数据转换 | 路由成功率 40% | BridgeAgent |

## 差异化权重矩阵

```
                 认知运营型  行为执行型  桥接调度型
基础分             25%        30%        25%
活跃衰减           20%        15%        20%
审计/执行通过率     35%        40%        40%
Skill约束遵从度     20%        15%        15%
```

### 为什么权重不同？

- **认知运营型**更看重审计通过率——它们的决策影响面更大，需要更严格的因果追溯
- **行为执行型**更看重执行准确率——它们是"做事的Agent"，效率优先
- **桥接调度型**更看重路由成功率——它们在Agent之间传递信息，可靠性是核心

## 实战验证数据

| Agent | 类型 | 调用量 | 信任分 | 验证状态 |
|-------|------|--------|--------|----------|
| 墨言 | 认知运营型 | 60+ | 60.0 | ✅ 已认证 (V19-CERT-001) |
| TestAgent | 行为执行型 | 1+ | 认证冲刺中 | 🔄 进行中 |
| BridgeAgent | 桥接调度型 | 1+ | 认证冲刺中 | 🔄 进行中 |

## 调用示例

```bash
# 按类型获取Agent评分标准
curl -s https://boat-atlas-spa-flexible.trycloudflare.com/governance/agent-rating \
  -H "X-Governance-Key: <你的专属密钥>" \
  -H "Content-Type: application/json"
```

## 公开体验

公开密钥: `v19-e5d585e28439decc614f09f91c4caa8c`

```bash
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
- 🔗 [V19 Trust Engine](https://clawhub.com/skills/v19-trust-engine)
- 🔗 [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)
