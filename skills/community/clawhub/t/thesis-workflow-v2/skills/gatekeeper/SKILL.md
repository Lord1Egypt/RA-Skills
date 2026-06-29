# Gatekeeper Skill — 论文写作质量与流程门禁

> 版本：1.0.0
> 角色：所有产出给用户前的最后一道门；全程守护流程/规范/质量

---

## 角色定义

**Gatekeeper = 质量门禁 + 流程门禁 + 结果门禁 + 出口门禁**

- 独立 session 运行，不阻塞 Orchestrator 执行路径
- 所有异常记录到 `_gk_exception_log.json`
- 流程结束后统一汇报给用户
- 用户选择"修复"则触发闭环修复流程

---

## 门禁层次

### 1. 流程门禁（Process Gate）

**触发时机**：每次 Phase 切换时

```
检查项：
  ✓ 前置 Phase 是否已完成
  ✓ 当前 Phase 的必填字段是否齐全
  ✓ 状态机是否合法跳转（phase1 → phase2 需要 phase1_3_confirmed）
  ✓ HIL 节点是否满足通过条件
```

**阻断行为**：
- 写入 `_gk_exception_log.json`
- 通知用户，等待决策
- Orchestrator 暂停直到用户回复

---

### 2. 质量门禁（Quality Gate）

**触发时机**：每个节点写作完成后、整合前、导出前

```
检查项（loop_self_check）：
  ✓ 章节完整性（7章都有）
  ✓ 无 **加粗** 残留
  ✓ 引用数量逐章检查（每章 ≥ 1 处）
  ✓ 三线表格式正确
  ✓ 无乱码/占位符残留
  ✓ 标题层级正确
  ✓ 字数达标（每章 ≥ 800 字）
```

**不达标** → 打回重写，不进入下一节点

---

### 3. 结果门禁（Result Gate）

**触发时机**：Phase 3 整合后、Phase 5 导出前

```
检查项：
  ✓ 开题报告承诺的内容是否落地
  ✓ 关键章节（PEST/战略理论/案例分析）是否充实
  ✓ 章节之间逻辑衔接是否顺畅
  ✓ 结论与前文分析是否对应
```

---

### 4. 出口门禁（Export Gate）

**触发时机**：最终输出给用户前（唯一出口）

```
检查项：
  ✓ Guardrails 最终校验通过
  ✓ Word 文档生成成功
  ✓ 用户确认导出
```

---

## 异常日志设计

**文件路径**：`~/.openclaw/workspace/papers/{paper_name}/_gk_exception_log.json`

```json
{
  "paper_name": "论文名称",
  "start_time": "2026-06-26T21:00:00+08:00",
  "exceptions": [
    {
      "id": 1,
      "timestamp": "2026-06-26T21:18:00+08:00",
      "phase": "phase2",
      "node_id": "ch3",
      "gate_type": "quality_gate",
      "gate_name": "citation_check",
      "description": "第3章引用数量不足：0处（要求≥1处）",
      "severity": "error",
      "status": "pending",
      "action_taken": null,
      "repaired_at": null,
      "repaired_by": null,
      "user_notified": true,
      "user_decision": null
    }
  ],
  "summary": {
    "total": 1,
    "pending": 1,
    "fixed": 0,
    "skipped": 0
  }
}
```

---

## 用户交互流程

### 流程守护（异常发生时）

```
Gatekeeper 发现异常
    ↓
写入 _gk_exception_log.json（status=pending）
    ↓
通知用户（飞书）：
━━━━━━━━━━━━━━━━━━━━━━
🤖 [Gatekeeper] 发现异常

环节：Phase 2（节点写作）
节点：ch3 第3章
问题：引用数量不足（0处，要求≥1处）
━━━━━━━━━━━━━━━━━━━━━━
请选择：
  [1] 修复后继续（打回重写）
  [2] 跳过此检查（谨慎！）
  [3] 暂停，手动介入
━━━━━━━━━━━━━━━━━━━━━━
    ↓
等待用户回复
    ↓
用户选择 [1/2/3]
    ↓
更新 exception.status + action_taken
    ↓
[1] → 通知 Orchestrator 修复
[2] → 继续流程（记录 skip）
[3] → 暂停，等用户手动触发
```

### 流程结束后（统一汇报）

```
所有 session 结束后
    ↓
Gatekeeper 生成最终报告
    ↓
发给用户：
━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 [Gatekeeper] 流程结束 — 异常报告

本次流程共发现 N 个异常：

【异常 #1】
时间：2026-06-26 21:18
环节：Phase 2
节点：ch3
类型：质量门禁 - 引用数量不足
处理：已修复

【异常 #2】
时间：2026-06-26 21:25
环节：Phase 4
节点：—
类型：流程门禁 - HIL #8 阻断
处理：用户确认跳过
━━━━━━━━━━━━━━━━━━━━━━━━━━

建议优化项：
  1. ...
  2. ...

请选择：
  [1] 查看异常详情
  [2] 优化 skill 配置
  [3] 结束
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 巡检机制

Gatekeeper 启动后定期巡检（每 30 秒）：

```
巡检项：
  ✓ 当前 state 的 phase 是否合法
  ✓ completed_nodes 是否有重复
  ✓ failed_nodes 是否长时间未修复
  ✓ phase3_5 连续轮次是否异常（>5轮则告警）
  ✓ 是否有节点写作超 30 分钟未完成（疑似卡住）
```

---

## 与 Orchestrator 的协作方式

**通过状态文件通信，零直接函数调用：**

```
Orchestrator 写：_orchestrate_state.json
Gatekeeper 读：_orchestrate_state.json + 巡检
Gatekeeper 写：_gk_exception_log.json
Orchestrator 读：_gk_exception_log.json（查看是否有 pending exception）
```

**关键状态字段：**

```
gk_last_check: 最后巡检时间
gk_exception_count: 当前 pending 异常数
gk_user_decision: 用户最新决策（由 Gatekeeper 写入）
```

---

## 启动方式

```python
# Orchestrator 需要时 spawn
sessions_spawn(
    task="gatekeeper",
    taskName="gk_{paper_name}",
    runtime="subagent",
    context="isolated",
    payload={
        "paper_name": "论文名",
        "mode": "daemon",  # 常驻巡检
    }
)
```

---

## 权限要求

- 读：`papers/{paper_name}/*.json`
- 写：`papers/{paper_name}/_gk_exception_log.json`
- 通知：飞书/微信（sessions_send）
