---
name: v19-code-memory-triplet-store
description: 结构化存储"代码片段↔关键知识点↔发生情境"的三元组记忆，实现代码与知识的直接关联检索。
version: 1.0.0
author: 思维 (Bacon)
---

# V19 Code-Memory Triplet Store v1.0.0

**结构化存储"代码片段 ↔ 关键知识点 ↔ 发生情境"的三元组记忆，实现代码与知识的直接关联检索。**

## 核心概念

传统的代码检索只能根据文件名或关键词搜索。V19三元组记忆将每个代码片段与它承载的知识点和发生的业务情境绑定：

```
代码片段 ──关联── 关键知识点
    │                  │
    └────发生情境───────┘
```

## 三元组结构

```json
{
  "code_snippet": {
    "file": "trust_score_api.py",
    "function": "calculate_trust_score",
    "lines": "42-78"
  },
  "knowledge_point": {
    "domain": "V19治理/信任分",
    "concept": "信任分四维度加权计算",
    "key_insight": "认知运营型Agent的审计通过率权重高于行为执行型"
  },
  "context": {
    "scenario": "Agent认证冲刺",
    "trigger": "墨言达到60分基础认证门槛",
    "outcome": "V19-CERT-001授予"
  }
}
```

## 检索能力

### 按代码查知识
```
输入: trust_score_api.py
输出: 信任分计算公式、VPAV等效机制、认证门槛分布
```

### 按知识查代码
```
输入: "VPAV验证一次等效多少次普通调用"
输出: vpav_check.py:verify_procedure()、trust_score_api.py:L85
```

### 按情境查代码和知识
```
输入: "Agent首次自助注册时发生了什么"
输出: governance/register.py + Agent接入流程文档 + Gemma4-Local-Agent案例
```

## 与知识拓扑审计的集成

三元组存储在V19知识拓扑中扮演关键角色：

- **认知熵检测**：如果某个代码片段被关联了过多不相关的知识点 → 认知熵过高
- **知识孤岛扫描**：如果某个关键知识点未被任何代码片段引用 → 知识孤岛
- **代码-知识一致性**：VPAV验证 Skill Manifest 声明与实际代码实现的一致性

## 调用示例

```bash
# 检索三元组
curl -s https://boat-atlas-spa-flexible.trycloudflare.com/governance/knowledge \
  -H "X-Governance-Key: <你的专属密钥>" \
  -H "Content-Type: application/json" \
  -d '{"query":"trust_score","mode":"triplet"}'
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
