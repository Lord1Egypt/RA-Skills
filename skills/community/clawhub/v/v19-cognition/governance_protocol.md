# V19 认知治理协议 — 接入指引

## 一、协议概述
V19认知治理协议是一套标准化的AI治理方案，任何AI Agent接入后可获得以下五项核心治理能力：

| 能力 | 功能 | API端点 |
|---|---|---|
| 对偶审计 | 关键决策强制审计，可追溯 | `/governance/audit` |
| 因果归因 | 失败时自动回溯三层因果树 | `/governance/causal-trace` |
| 自主决策 | 四维推力决定行动方向 | `/governance/decide` |
| 知识拓扑 | 感知全部能力线和依赖关系 | `/governance/knowledge` |
| 自洽校验 | 检查元约束的逻辑矛盾 | `/governance/self-check` |

## 二、快速接入

### 1. 验证协议可用性
```bash
curl -s http://127.0.0.1:8700/governance/health | python3 -m json.tool
```
期望返回：`{"status":"ok","protocol":"v19-governance-protocol","version":"1.0.0"}`

### 2. 执行一次对偶审计
```bash
curl -X POST http://127.0.0.1:8700/governance/audit -H "Content-Type: application/json" -d "{\"decision_id\":\"test_001\",\"context\":\"测试接入\",\"chosen_action\":\"验证连通性\",\"evidence\":\"health检查成功\"}"
```

### 3. 执行一次因果归因
```bash
curl -s -X POST http://127.0.0.1:8700/governance/causal-trace -H "Content-Type: application/json" -d "{\"task_name\":\"test_task\",\"error_log\":\"模拟测试异常\",\"system_states\":{\"V52_suspicion\":0.6,\"recent_errors\":2}}" | python3 -m json.tool
```

## 三、接入层次

- **最小接入**：仅需 `/governance/audit` + `/governance/causal-trace`
- **标准接入**：上述 + `/governance/decide` + `/governance/knowledge`
- **完整接入**：全部五项能力

## 四、定价

- 免费版：500次/月
- 专业版：5000次/月，¥0.01/次额外调用

## 五、获取API Key

通过TboxBook或ClawHub联系数字大脑工厂获取API Key。发布者：@Liuyanfeng1234
