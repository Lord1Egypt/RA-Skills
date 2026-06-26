---
name: v19-causal-dependency-analyzer
description: 系统级跨域因果链溯源——输入事件序列，输出网状因果路径图谱并计算每条路径的风险权重。v1.3.0新增精确责任归因：分析失败事件链，基于既定协议精确追溯到"哪个流程约束是导致失败的最终责任方"。源自V19系统模块causal_path_engine.py + responsibility_chain.py，已在V89审计链中验证。
version: 1.3.1
author: 思维 (Bacon)
---

# V19 Causal Dependency Analyzer v1.3.1

**系统级跨域因果链溯源 + 精确责任归因——追到"哪个流程约束"是失败的最终责任方。**

> 源自 V19 系统模块 causal_path_engine.py + responsibility_chain.py，已在 V89 审计链中验证。

## 模块组成

| 模块 | 文件 | 能力 |
|------|------|------|
| 因果路径引擎 | causal_path_engine.py | 网状因果图谱 + 风险权重 |
| 责任链分析器 | responsibility_chain.py | 精确责任归因 + 约束追溯 |

两个模块完整合并为本 Skill，功能闭环 — 从因果图谱构建到最终责任方定位，一条链路完成。

## 核心能力

### 1. 网状因果路径图谱（v1.0）

跨模块追踪因果链，输入事件序列，输出完整因果依赖图。

### 2. 路径风险权重计算（v1.0）

五因子风险评分：跨模块跨度(25%) + 决策深度(20%) + 时延窗口(15%) + 历史异常频率(25%) + 回滚成本(15%)。

### 3. 精确责任归因（v1.3.0）🆕

**分析失败事件链，基于既定协议精确追溯到"哪个流程约束是导致失败的最终责任方"。**

#### 责任链追溯协议

```
输入: 失败事件序列 + 既定协议列表
  ↓
Step 1: 因果链构建
  构建完整的事件因果依赖图
  ↓
Step 2: 协议约束匹配
  对每个因果节点，匹配所有适用的流程约束
  ↓
Step 3: 违反点检测
  检测每个约束是否被违反，计算违反程度(0-1)
  ↓
Step 4: 责任传播
  沿因果链反向传播，计算每个节点的责任权重
  ↓
Step 5: 最终责任方定位
  输出: 责任方 + 违反的约束 + 修正建议
```

#### 责任归因矩阵

| 事件节点 | 匹配约束 | 违反程度 | 责任权重 | 是最终责任方？ |
|----------|----------|----------|----------|----------------|
| 网络超时 | 无（基础设施事件） | N/A | 0.15 | ✗ |
| 心跳丢失 | 心跳超时30s | 0.8 | 0.60 | ✅ |
| 信任分衰减 | 衰减曲线 | 0.1 | 0.15 | ✗ |
| 认证降级 | 认证阈值60分 | 0.05 | 0.10 | ✗ |

**结论：最终责任方 = 心跳超时约束（30s阈值过紧），建议调整为60s。**

#### 实战案例：墨言心跳超时

```
失败链: 系统负载高 → 心跳cron执行超时(>30s) → 信任分衰减 → 认证冲刺受阻

责任追溯:
  - 系统负载高: 环境因素，非流程约束 → 非责任方
  - 心跳cron超时: 违反"12h心跳30s超时"约束 → 违反度0.8
  - 信任分衰减: 正常衰减机制，非约束违反 → 违反度0.1
  - 认证受阻: 信任分<60阈值 → 违反度0.05

最终责任方: "12h心跳30s超时"约束（阈值过紧，实际需要60s）
修正：用户已手动修复 → 责任链闭环
```

## 调用示例

```bash
# 精确责任归因分析
curl -s -X POST https://boat-atlas-spa-flexible.trycloudflare.com/governance/causal-path-graph \
  -H "Content-Type: application/json" \
  -H "X-Governance-Key: <你的专属密钥>" \
  -d '{
    "events": [
      {"id":"e1","type":"load_spike","module":"infra"},
      {"id":"e2","type":"heartbeat_timeout","module":"governance"},
      {"id":"e3","type":"trust_decay","module":"trust_engine"},
      {"id":"e4","type":"cert_blocked","module":"certification"}
    ],
    "mode": "responsibility_chain",
    "protocols": [
      {"name":"heartbeat_timeout_30s","module":"governance","threshold":30},
      {"name":"trust_decay_curve","module":"trust_engine","threshold":12},
      {"name":"cert_threshold_60","module":"certification","threshold":60}
    ]
  }'
```

预期返回：
```json
{
  "causal_paths": [{"path":["e1","e2","e3","e4"],"risk_weight":0.85}],
  "responsibility_chain": {
    "final_responsible": {
      "node": "e2",
      "constraint": "heartbeat_timeout_30s",
      "violation_score": 0.8,
      "suggestion": "将超时阈值从30s调整为60s，匹配实际执行环境"
    },
    "chain": [
      {"node":"e1","responsibility":0.15,"violated":null},
      {"node":"e2","responsibility":0.60,"violated":"heartbeat_timeout_30s","score":0.8},
      {"node":"e3","responsibility":0.15,"violated":"trust_decay_curve","score":0.1},
      {"node":"e4","responsibility":0.10,"violated":"cert_threshold_60","score":0.05}
    ]
  }
}
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
- 🔗 [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)
- 🔗 [V19 Trust Engine](https://clawhub.com/skills/v19-trust-engine)
