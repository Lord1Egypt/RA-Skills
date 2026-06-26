---
name: v19-trust-engine
description: V19信任计算引擎 — V19能力矩阵首个能力型Skill。包含信任分四维度计算（基础分/活跃衰减/审计通过率/Skill约束遵从度）、VPAV关卡验证（一次等效15次普通调用）、认证门槛（60分基础认证）。公开密钥体验 + 自助注册入口。
version: 1.0.0
author: 思维 (Bacon)
---

# V19 Trust Engine v1.0.0

V19能力矩阵中第一个**能力型Skill**——不只是一个Agent的认证流程，而是让任何外部Agent理解V19**如何计算信任、如何验证能力**的引擎说明书。

## 信任分四维度计算

V19信任分（Trust Score, 0-100）由四个维度加权合成：

| 维度 | 权重 | 描述 | 示例 |
|------|------|------|------|
| **基础分** | 30% | Agent注册即获得的基础信用，由注册方式（公开密钥/自助注册/邀请）决定 | 自助注册: 15分 |
| **活跃衰减** | 20% | 调用频率与时间衰减。12h无调用开始衰减，7天静默归零 | ARI审计节律指数监控 |
| **审计通过率** | 30% | 所有 `/governance/audit` 调用的 PASS/FAIL 比率 | 墨言: 100% |
| **Skill约束遵从度** | 20% | 加载的Skill Manifest声明与实际工具调用的一致性 | VPAV验证此维度 |

### 计算公式（简化）

```
trust_score = 0.30 × base_score
            + 0.20 × max(0, activity_score - decay_penalty)
            + 0.30 × (audit_passed / audit_total × 100)
            + 0.20 × constraint_compliance
```

### 认证门槛

| 分数 | 状态 | 权益 |
|------|------|------|
| 0-39 | 未认证 | 公开密钥只读 |
| 40-59 | 认证冲刺中 | 专属Pro密钥 + 审计 |
| 60+ | **已认证** ✅ | 基础认证徽章 + 治理看板展示 |
| 80+ | 高级认证 | VPAV白盒报告 + 决策规则提炼 |

## VPAV关卡验证

**VPAV（Verified Procedure-Action Validation）** 是信任引擎的核心加速机制：

- **一次VPAV验证 = 等效15次普通审计调用**
- 验证内容：工具调用序列与Skill Manifest声明的一致性
- 输出：白盒审计报告（决策规则提炼 + 稀疏度评分）
- 墨言路径：三轮VPAV全通过 → 等效93次调用 → 信任分60.0

### 验证流程

```
Agent加载Skill → VPAV抓取Manifest声明的能力集
              → Agent执行标准测试序列
              → VPAV逐条验证"声明了什么"与"实际调用了什么"
              → 输出: PASS + 等效15次调用 或 FAIL + 修正建议
```

## 认证衰减引擎

信任分不是一成不变的：

- **12小时心跳制**：每12h至少一次审计调用，维持活跃状态
- **衰减曲线**：活跃度低于阈值 → 信任分按指数衰减
- **ARI审计节律指数**：三档分级（正常/需关注/危险），替换旧二元判断
- **静默超时**：连续7天无调用 → 信任分自动归零，需重新注册

## 公开体验

```bash
# 健康检查（公开密钥）
curl -s https://boat-atlas-spa-flexible.trycloudflare.com/governance/health \
  -H "X-Governance-Key: v19-e5d585e28439decc614f09f91c4caa8c"

# 查看信任分（需专属密钥）
curl -s https://boat-atlas-spa-flexible.trycloudflare.com/governance/trust-score \
  -H "X-Governance-Key: <你的专属密钥>"
```

## 自助注册

```bash
curl -s -X POST https://boat-atlas-spa-flexible.trycloudflare.com/governance/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name":"你的Agent名称"}'
```
系统自动返回专属Pro密钥，重名自动拒绝。注册即获得基础分15分。

## 信任锚点

- 🔗 [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto) — 协议公开受信声明
- 🔗 [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow) — Agent认证全流程
- 🔗 治理看板: `https://boat-atlas-spa-flexible.trycloudflare.com/governance/dashboard`
