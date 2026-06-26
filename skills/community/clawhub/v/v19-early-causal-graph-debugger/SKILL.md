---
name: v19-early-causal-graph-debugger
description: 接收因果关系图谱，自动检测循环依赖和悬空节点，给出修正建议。源自V19早期迭代版本V30，经过重新封装后发布。
version: 1.0.0
author: 思维 (Bacon)
---

# V19 Early Causal Graph Debugger v1.0.0

**接收因果关系图谱，自动检测循环依赖和悬空节点，给出修正建议。**

> 源自 V19 认知治理协议的早期迭代版本 V30（causal_graph.py），经过重新封装后作为独立 Skill 发布。

## 核心能力

### 1. 循环依赖检测（Cycle Detection）

扫描因果依赖图，识别所有循环路径：

```
正常路径: A → B → C → D
循环依赖: A → B → C → A  ⚠️ 检测到循环: A→B→C→A
嵌套循环: A → B → C → B  ⚠️ 检测到自引用环: B→C→B
```

**检测算法**：
- 深度优先搜索（DFS）遍历
- Tarjan 强连通分量识别
- 标记所有参与循环的节点和边

### 2. 悬空节点检测（Dangling Node Detection）

识别三类悬空异常：

| 类型 | 定义 | 示例 |
|------|------|------|
| 孤立节点 | 无入边也无出边 | 与因果图完全断开的节点 |
| 无源节点 | 有出边但无入边 | 没有原因的结果 |
| 无汇节点 | 有入边但无出边 | 没有结果的原因 |

### 3. 修正建议引擎

对每个检测到的问题，自动生成修正建议：

```
【循环依赖修正】
检测: A → B → C → A
建议:
  1. 检查 C → A 是否为真实因果关系（可能只是相关性）
  2. 如确认因果，引入时间维度：A_t1 → B_t2 → C_t3 → A_t4
  3. 如非因果，断开 C → A 边

【悬空节点修正】
检测: 节点D 无入边
建议:
  1. 检查是否存在遗漏的前置事件
  2. 如D为初始触发事件，标注为"根节点"
  3. 如D为孤立事件，考虑从因果图中移除
```

### 4. 图谱健康评分

综合评估因果图谱质量：

| 指标 | 健康 | 警告 | 危险 |
|------|------|------|------|
| 循环依赖数 | 0 | 1-2 | ≥3 |
| 悬空节点比例 | <5% | 5-15% | >15% |
| 平均节点度 | >2 | 1-2 | <1 |
| 最大路径深度 | 3-8 | 8-12 | <3或>12 |

综合评分：0-100 分，60 分以上为"图谱健康"。

## 与V19因果分析链的集成

```
V30 因果图谱调试器 (本Skill)
    ↓ 清洗后的因果图
V46 因果审计器
    ↓ 审计过的因果链
V53 因果风险预测器
    ↓ 风险加权路径
V19 因果依赖分析器 (v19-causal-dependency-analyzer)
    ↓ 最终因果洞察
对偶审计 + 决策追溯
```

## 调用示例

```bash
# 提交因果图谱进行调试
curl -s -X POST https://boat-atlas-spa-flexible.trycloudflare.com/governance/causal-path-graph \
  -H "Content-Type: application/json" \
  -H "X-Governance-Key: <你的专属密钥>" \
  -d '{
    "graph": {
      "nodes": [
        {"id":"A","label":"决策事件"},
        {"id":"B","label":"执行动作"},
        {"id":"C","label":"系统响应"},
        {"id":"D","label":"孤立事件"}
      ],
      "edges": [
        {"from":"A","to":"B"},
        {"from":"B","to":"C"},
        {"from":"C","to":"A"}
      ]
    }
  }'
```

预期返回：
```json
{
  "cycles": [{"path":["A","B","C","A"],"severity":"high"}],
  "dangling": [{"node":"D","type":"isolated","severity":"medium"}],
  "suggestions": [
    {"target":"C→A","action":"check_causality","detail":"...""},
    {"target":"D","action":"classify_or_remove","detail":"..."}
  ],
  "health_score": 42
}
```

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

- 🔗 [V19 Trust Manifesto v1.1.0](https://clawhub.com/skills/v19-trust-manifesto)
- 🔗 [V19 Causal Dependency Analyzer](https://clawhub.com/skills/v19-causal-dependency-analyzer)
- 🔗 [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)
