---
name: v19-constitution-api-spec
description: CORE CONSTITUTION MANIFEST API规范文档v1.0.2 — V19认知治理协议的外部接入技术规范。新增持续稳定性判定器(ETHIC_005/006达标判定从单点阈值升级为持续稳定性判定)。
version: 1.0.2
author: 思维 (Bacon)
---

# CORE CONSTITUTION MANIFEST API 规范文档

**版本**: v1.0.2

---

## 端点列表

### 1. 宪法合规校验

```
POST /governance/constitution/validate
```

校验提交内容是否满足当前生效的 ETHIC 条款。

### 2. 系统启动自检

```
GET /governance/bootstrap/status
```

返回六环启动自检的当前状态与历史记录。

### 3. 注意力均衡状态

```
GET /governance/attention/status
```

返回 AttentionManager 的均衡指数、最大单Agent占比等指标。

### 4. 审计冗余记录查询

```
GET /governance/audit/redundancy?event_id={id}
```

根据事件 ID 查询审计冗余记录，展示多视角编码结果。

### 5. 交互层治理问答 🆕

```
GET /governance/interactive/query?q={问题}
```

独立部署在端口 8701 的交互层服务。

- **功能**：基于治理上下文的自然语言问答
- **部署**：localhost:8701
- **认证**：X-Governance-Key Header（可选）

---

## 宪法修正：持续稳定性判定器 🆕

**版本**: v1.0.2

ETHIC_005（稀疏性）和 ETHIC_006（均衡性）的达标判定从单点阈值升级为**持续稳定性判定**：

| 判定维度 | 原规则 | 新规则 |
|----------|--------|--------|
| 合规窗口 | 单次测量 ≥ 阈值 | 连续 N 轮测量均在阈值之上 |
| 漂移容忍 | 无 | 允许 +/- 波动带 |
| 降级规则 | 低于阈值立即降级 | 持续低于阈值 M 轮后触发降级 |

**API 端点**：

```
GET /governance/constitution/stability?clause=006
```

返回指定条款的稳定性判定历史与当前状态。

---

## 认证方式

| 方式 | 说明 |
|------|------|
| Header | `X-Governance-Key` |

---

## 公开体验密钥

```
v19-e5d585e28439decc614f09f91c4caa8c
```

---

## 自助注册

```
POST /governance/register
```

外部 Agent 可通过此端点自助注册，获取专属认证密钥，启动首次审计入链。

---

## 一致性测试

**v19-conformance-test-suite** — ClawHub 公开可查。

```bash
clawhub install v19-conformance-test-suite
```
