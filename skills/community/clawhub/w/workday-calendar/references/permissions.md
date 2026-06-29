# 基于 skill-standardization 渐进式披露规范的权限说明

本文档由 `skill-standardization` 权限扫描器自动维护。

## 风险等级

**LOW**（实际权重: 0.2）

## 权限总览

| 权限类别 | 涉及项数 | 风险等级 |
|-----------|----------|----------|
| `subprocess_call` | 0 项 | ✅ LOW |
| `file_delete` | 0 项 | ✅ LOW |
| `network_access` | 1 项 | 🔴 HIGH |
| `sensitive_access` | 0 项 | ✅ LOW |
| `critical_write` | 0 项 | ✅ LOW |

## 高权限操作说明

- **网络访问**（1 项，silent）


## 权限详细说明

### 子进程调用（subprocess）

**无**。


### 文件删除

**无**。


### 网络访问（1 项）

> **功能说明**：技能需要通过网络连接到外部服务或远程仓库。
> **授权方式**：silent

| 文件 | 行号 | 匹配内容 | 功能说明 |
|------|------|----------|----------|
| `scripts\settings.py` | 93 | `urllib` | 自动化技能：中风险静默执行，仅记录 |


### 敏感信息访问

**无**。


### 关键位置写入

**无**。


## 授权方式说明

- **immediate（即时授权）**：每次执行前需获得用户批准
- **unified（统一授权）**：首次执行前获得用户批准，后续不再询问
- **silent（静默授权）**：无需用户交互，自动执行并记录

<!-- fp:risk=LOW|sensitive=0|critical_write=0|network=1|delete=0|subprocess=0|issues=1 -->
---

# 权限说明

> 由 `permission_checker.py` 扫描生成，基于脚本实际文件操作行为计算风险权重。

## 风险等级

`low`（权重 **0.00%**）

## 扫描摘要

| 项目 | 值 |
|------|-----|
| 扫描文件数 | 1 |
| 扫描行数 | 1348 |
| 风险等级 | low |
| 权重 | 0.00% |
| 高权限操作 | 无 |

## 权限操作清单

脚本 `scripts/workday_calendar.py` 文件操作均为**数据读写**（JSON 配置文件），无删除/网络/子进程操作：

| 操作 | 文件路径 | 权限 |
|------|----------|--------|
| 读假日配置 | `.standardization/workday-calendar/data/holiday_intervals_YYYY.json` | 📖 读 |
| 写假日配置 | `.standardization/workday-calendar/data/holiday_intervals_YYYY.json` | ✏️ 写 |
| 读补班配置 | `.standardization/workday-calendar/data/compensatory_days_YYYY.json` | 📖 读 |
| 写补班配置 | `.standardization/workday-calendar/data/compensatory_days_YYYY.json` | ✏️ 写 |
| 读周末配置 | `.standardization/workday-calendar/data/weekend_config.json` | 📖 读 |
| 写周末配置 | `.standardization/workday-calendar/data/weekend_config.json` | ✏️ 写 |
| 读日程数据 | `.standardization/workday-calendar/data/schedule_events.json` | 📖 读 |
| 写日程数据 | `.standardization/workday-calendar/data/schedule_events.json` | ✏️ 写 |

## 授权方式

**`silent`**（静默执行，无需用户授权）

理由：
- 权重 0.00%，无高权限操作
- 仅读写本地 JSON 数据文件  
- 无网络访问、无子进程调用、无文件删除操作  

## 权重说明

权重 = Σ(操作风险分值) / 100，上限 100%。

本技能仅做本地 JSON 数据读写，风险分值为 0，故权重 0.00%。
