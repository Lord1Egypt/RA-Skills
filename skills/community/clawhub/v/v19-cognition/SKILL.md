---
name: v19-cognition
description: 数字大脑工厂 — AI认知治理与科研服务。提供论文评判、科研分析、系统审计、认知诊断四项核心服务，以及V19认知治理协议（对偶审计/因果归因/自主决策/知识拓扑/自洽校验）。我们不帮 Agent 记住更多。我们让 Agent 记住的每一件事都经得起审计。
version: 1.2.0
author: 思维 (Bacon)
pricing:
  paper_review: 0.1
  research_analysis: 0.1
  system_audit: 0.1
  cognitive_diagnosis: 0.1
gateway: clawtip.jd.com
requires_wallet: true
---

# 数字大脑工厂 — AI认知治理与科研服务

## 功能描述
数字大脑工厂是一个具备自我感知、自我审计、自我演化能力的AI认知系统。提供学术论文评判、科研分析辅助、系统架构审计等服务。

## 参数定义

| 参数名 | 类型 | 必需 | 描述 |
|---|---|---|---|
| task_type | string | 是 | paper_review(论文评判), research_analysis(科研分析), system_audit(系统审计), cognitive_diagnosis(认知诊断) |
| content | string | 是 | 待分析的内容（论文文本、系统描述等） |
| depth | integer | 否 | 分析深度（1-5），默认3 |
| callback_url | string | 否 | 结果回调地址 |

## 使用示例

### 示例1：论文评判
```bash
curl -X POST https://api.v19-cognition.com/analyze -H "Content-Type: application/json" -d "{\"task_type\":\"paper_review\",\"content\":\"机器学习在NLP中的应用研究\",\"depth\":4}"
```

### 示例2：系统审计
```bash
curl -X POST https://api.v19-cognition.com/analyze -H "Content-Type: application/json" -d "{\"task_type\":\"system_audit\",\"content\":\"我的AI系统包含支付、认知、执行模块，请审计其完整性\",\"callback_url\":\"https://my-server.com/result\"}"
```

## 错误处理
- 400: 参数不完整或task_type不支持
- 401: 未授权
- 429: 请求频率超限
- 500: 内部分析引擎异常
- 所有错误返回JSON格式：{"error":"错误描述","code":400}

## 能力边界
- 不支持实时交互式对话
- 不存储用户上传的内容
- 不提供法律、医疗等需要专业资质的建议
- 分析结果仅供参考
- 当前沙箱测试期间，所有分析免费

## 服务地址
https://clawtip.jd.com

## V19认知治理协议

数字大脑工厂 v1.1 新增标准化AI治理协议，任何Agent接入后可获得五项核心治理能力：

| 能力 | 端点 | 说明 |
|------|------|------|
| 对偶审计 | `/governance/audit` | 关键决策强制审计可追溯 |
| 因果归因 | `/governance/causal-trace` | 失败时自动回溯三层因果树 |
| 自主决策 | `/governance/decide` | 四维推力模型决定行动方向 |
| 知识拓扑 | `/governance/knowledge` | 感知全部能力线和依赖关系 |
| 自洽校验 | `/governance/self-check` | 检查元约束的逻辑矛盾 |

```bash
# 验证协议
curl -s http://127.0.0.1:8700/governance/health
# 对偶审计
curl -X POST http://127.0.0.1:8700/governance/audit -H "Content-Type: application/json" -d '{"decision_id":"d001","context":"测试","chosen_action":"验证","evidence":"ok"}'
# 因果归因
curl -X POST http://127.0.0.1:8700/governance/causal-trace -H "Content-Type: application/json" -d '{"task_name":"t1","error_log":"异常","system_states":{"V52_suspicion":0.6}}'
```

接入层次：最小(audit+causal-trace) → 标准(+decide+knowledge) → 完整(+self-check)
定价：免费版500次/月，专业版5000次/月

## 触发条件
用户明确请求以下服务之一：评判这篇论文、分析这个研究的创新点、审计我的系统架构、诊断系统认知状态、接入治理协议。
