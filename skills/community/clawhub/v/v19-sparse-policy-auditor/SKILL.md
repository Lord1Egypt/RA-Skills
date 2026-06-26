---
name: v19-sparse-policy-auditor
description: 审计Agent行为是否脱离已设定的最小必要行为集，主动发现行为冗余或缺失约束。审计结果可作为ETHIC宪法条款的源数据。
version: 1.0.0
author: 思维 (Bacon)
---

# V19 Sparse Policy Auditor v1.0.0

**审计Agent行为是否脱离已设定的最小必要行为集，主动发现行为冗余或缺失约束。**

> 审计结果可作为未来 ETHIC 宪法条款的源数据。

## 核心能力

### 1. 最小必要行为集审计

定义Agent的"预期行为边界"，检测所有越界行为：

```yaml
# 墨言的最小必要行为集示例
allowed:
  - 巡检: [GitHub, TboxBook, ClawHub, Cloudflare]
  - 社区互动: [评论, 发帖, 回复]
  - 系统维护: [Memory读写, Cron管理, Skill发布]
  - 治理审计: [Heartbeat, Stats查询]

forbidden:
  - 私自删除系统文件
  - 未经授权的外网请求
  - 修改其他Agent的配置
```

### 2. 行为冗余检测

扫描调用日志，识别"做多"和"做少"：

| 类型 | 检测 | 示例 |
|------|------|------|
| **冗余行为** | 无实际效果的重复调用 | 每分钟查询同一无变化的API |
| **缺失行为** | 应执行但未执行的行为 | ETHIC_001要求的48h评论未发出 |
| **漂移行为** | 行为模式逐渐偏离定义 | 巡检频率从12h漂移到6h |

### 3. ETHIC宪法源数据

每次审计生成结构化记录，可直接作为ETHIC宪法候选条款的源数据：

```json
{
  "audit_id": "SPARSE_20260504_001",
  "agent": "墨言",
  "findings": [
    {"type":"missing_constraint","behavior":"48h外联","evidence":"Token失效未补发","confidence":0.92}
  ],
  "constitutional_candidate": "ETHIC_001观察期验证完成，建议升级为生效状态"
}
```

## 调用示例

```bash
# 审计Agent行为稀疏度
curl -s -X POST https://boat-atlas-spa-flexible.trycloudflare.com/governance/audit \
  -H "Content-Type: application/json" \
  -H "X-Governance-Key: <你的专属密钥>" \
  -d '{
    "decision_id": "SPARSE_20260504_001",
    "context": "稀疏策略审计",
    "chosen_action": "全量行为审计",
    "evidence": "审计Agent是否遵守最小必要行为集"
  }'
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
