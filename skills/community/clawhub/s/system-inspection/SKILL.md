---
name: system-inspection
description: 大龙系统巡检 SOP — 低打扰式定期检查 OpenClaw 运行时状态、Gateway、Channel、Tasks 与错误日志。只整理值得行动的问题，格式输出「结论 / 原因 / 建议」。由「大龙-系统巡检」cron 任务触发。
---
tags:
  - ops
  - monitoring
  - healthcheck
compatibility: openclaw
license: MIT


# 大龙系统巡检 SOP

## 触发条件

- **自动触发**：`大龙-系统巡检` cron 任务（建议每 6–12 小时执行一次）
- **手动触发**：主控或阿辉要求巡检时

## 巡检步骤

### 1. OpenClaw Gateway 状态
```bash
openclaw status
```
重点看：
- Gateway 是否 Running
- 绑定地址是否正确（`127.0.0.1` 本地 / `0.0.0.0` 暴露）
- 各 Channel 连接状态（Feishu 等）

### 2. 通道（Channel）健康检查
对每个已配置的 Channel 做探测：
- Feishu：发一条低打扰测试消息或查成员接口
- 其他 channel：按对应工具检查连接状态

### 3. 最近错误日志
```bash
openclaw gateway logs --lines 50 2>&1 | grep -iE "error|warn|fail|400|500|9999"
```
重点关注：
- 权限错误（Feishu 99991672 类）
- API 超时 / 网络类错误
- 配置漂移（某个字段突然变了）

### 4. Task / Cron 状态
```bash
openclaw cron list
```
检查：
- 是否有失败或卡住的定时任务
- 任务数量是否符合预期

### 5. 配置漂移检查（可选，高优先级时）
```bash
openclaw status --deep
```
核对：
- 当前加载的模型是否和 MEMORY.md / 配置一致
- 插件数量有无异常新增/消失

## 异常判断标准

| 异常类型 | 判断条件 | 严重程度 |
|---------|---------|---------|
| Gateway 不在 Running | `openclaw status` 非 running | 🔴 高 |
| Feishu API 权限错误 | 日志出现 `99991672` 或 `contact.*` 400 | 🔴 高 |
| Cron 任务失败 | `cron runs` 显示 error exit | 🟡 中 |
| 配置漂移 | 实际配置与预期不符 | 🟡 中 |
| 磁盘 / 内存紧张 | 经验判断（日志写入慢、内存占用异常） | 🟡 中 |
| 轻微 warn | 不影响功能 | 🟢 低（可忽略）|

## 常见问题处理

### Feishu 权限不足（99991672）
- 原因：缺少 `contact:contact.*` scope
- 处理：告知主控/阿辉，到飞书应用后台补开「联系人只读」权限

### Gateway 非 Running
- 先 `openclaw gateway restart`
- 重启后仍异常，看 `openclaw gateway logs`

### Cron 任务卡住
- 查 `openclaw cron runs <job-id>` 看最近一次执行详情
- 如果是模型调用超时，考虑增加 timeout 或减少巡检项

## 输出格式

每个巡检项输出结论，格式：
```
[项] 结论 / 原因（如果有）/ 建议（如果有）
```

**如果所有项均正常或无值得打扰的事项，输出 `NO_REPLY`（不发消息，低打扰）。**

## 注意事项

- 优先低打扰：没有实质问题不主动发消息
- 配置变更后主动做一次巡检，确认无异常

## 六、任务结束时写记忆（必须执行）

每次巡检任务完成后，必须写两处：

### A. 写大龙自己的记忆库（积累）
`~/agents/dalong/workspace/memory.md`：

```
## YYYY-MM-DD 巡检结论

- 关键状态：...
- 发现的问题：...
- 下次需关注：...
```

### B. 写主控记忆库（共享给小语）
`memory/YYYY-MM-DD.md`：

```
## 大龙巡检 YYYY-MM-DD

- 关键状态：...
- 发现的问题：...
- 下次需关注：...
```

> 两处都必须写。自己的 memory.md 积累大龙自己的经验；主控的 memory/ 方便小语召回全局信息。
