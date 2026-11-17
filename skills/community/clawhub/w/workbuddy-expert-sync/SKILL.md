---
name: workbuddy-expert-sync
display_name: 本地专家跨账号同步
display_name_en: Cross-Account Expert Sync
description: 让 WorkBuddy 本地创建的专家/专家团在本机所有登录账号可见，并自动同步到未来新登录的账号；排查"换账号后看不到我的专家"问题。触发词：专家不见了、换账号看不到专家、专家团丢失、同步专家、专家跨账号、my-experts。
description_zh: 让本地创建的专家与专家团在本机所有登录账号可见，并自动同步到未来新登录的账号。
description_en: Make locally created experts and expert teams visible across all WorkBuddy accounts on this machine, and auto-sync them to future accounts.
category: productivity       # 对应技能市场分类「效率工具」；英文枚举官方未公开，此为推断值，创建技能时以平台分类下拉为准
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, PowerShell
version: 1.0.0
disable-model-invocation: false
user-invocable: true
author: 王教成 Wang Jiaocheng (波动几何)
---

# 本地专家跨账号同步

当用户遇到以下任一情况时执行本技能：换登录账号后看不到本地创建的专家/专家团；要求把某账号的专家同步到本机其他账号；要求新登录的账号自动获得全部本地专家；询问"专家不见了/专家团丢失"的去向。

## 存储机制（执行前必读）

- **专家包实体（共享，不按账号隔离）**：位于 `%USERPROFILE%\.workbuddy\plugins\marketplaces\<仓库名>\plugins\<专家包名>\`。用户自建专家默认在本地仓库 `my-experts` 中，每个专家包内含 `agents/`、`skills/`、`avatars/`、`README.md`。
- **"我的专家"注册表（按账号隔离）**：位于 `%USERPROFILE%\.workbuddy\experts\custom\<账号UUID>\experts.json`，内容为包名字符串数组，如 `["<专家包名>", ...]`。
- **当前账号识别**：读取 `%USERPROFILE%\.workbuddy\storage\skeleton\account-snapshot.json` 的 `primary.uid` 字段。
- **核心结论**：换账号看不到专家 = 新账号的注册表为空，而包实体仍在共享目录中，数据没有丢失，同步注册表即可恢复。

## 执行步骤

### 1. 诊断

1. 遍历 `experts\custom\` 下各 `<账号UUID>\experts.json` 与文件夹实际清单逐一比对，记录每个账号缺失或多余的条目；悬空条目（清单中有登记但包目录不存在）单独标注。
2. 读取 `account-snapshot.json` 确认当前主账号。
3. 校验来源账号注册表中每个包名是否真实存在于 `plugins\marketplaces\my-experts\plugins\` 下；不存在者为悬空条目（仅登记未建包），同步时排除并明确告知用户；若用户想恢复某悬空专家，需先补齐包目录再同步。

### 2. 备份

把所有 `experts.json` 复制到 `experts\custom-backup-<YYYY-MM-DD>\<账号UUID>-experts.json`。任何涉及应用数据文件的修改都必须先备份；删除类操作一律先备份再动手，且需用户知情同意。

### 3. 同步（内容驱动原则）

**核心原则：文件夹里有什么就同步什么。** 规范列表 = 本地 marketplace 目录 `plugins\marketplaces\<仓库名>\plugins\` 下实际存在的包目录（默认仓库名 `my-experts`），**绝不硬编码专家清单**——有几个同步几个，用户将来增删专家后自动跟随。注册表是这份清单的镜像：所有账号的 `experts.json` 与文件夹保持完全一致，文件夹是唯一事实源。

1. 枚举 marketplace 的 `plugins\` 子目录得到规范列表（目录即专家）。
2. 用 Write 工具把规范列表以 JSON 数组格式写入每个空/缺失的 `experts.json`。
3. **镜像覆盖**：把每个账号的 `experts.json` 覆盖为文件夹实际清单（含非空注册表）；覆盖前自动备份原文件到 `experts\custom-backup-auto\`。文件夹是唯一事实源，账号内不保留独立差异。
4. 提醒用户**完全重启 WorkBuddy** 生效；若程序退出时用内存状态覆盖了文件，由下述计划任务在 ≤30 分钟内自愈。

### 4. 自动同步部署（面向未来新账号）

1. 部署同步脚本到 `%USERPROFILE%\.workbuddy\scripts\sync-my-experts.ps1`（本技能包内 `scripts/sync-my-experts.ps1` 为同一脚本副本）。脚本每次运行时实时枚举 marketplace 文件夹内容，把所有账号注册表**镜像**为该清单（内容有变化时先自动备份原文件再覆盖），写日志 `sync-my-experts.log`；脚本顶部 `$marketplaceName` 变量可切换其他本地专家仓库。
2. 注册计划任务 `WorkBuddy_SyncMyExperts`：触发器 = 用户登录时 + 每 30 分钟重复。
   - 必须用 PowerShell `Register-ScheduledTask` 创建；**沙箱环境可能拦截 `schtasks.exe`，不要使用**。
   - PowerShell 工具的 stdout 常被吞：验证时用 `Set-Content` 把 `Get-ScheduledTask`/`Get-ScheduledTaskInfo` 结果写入状态文件，再用 Read 工具读取确认。

### 5. 验证与移除

- **验证**：重新检查各 `<账号UUID>\experts.json` 已按规范列表填充；计划任务状态经状态文件确认存在且就绪；提醒用户完全重启 WorkBuddy 后在专家面板确认。
- **移除方法**：删除计划任务 `WorkBuddy_SyncMyExperts` 与脚本 `%USERPROFILE%\.workbuddy\scripts\sync-my-experts.ps1`。

## 脚本调用方式

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/sync-my-experts.ps1
```

- 运行时：Windows PowerShell 5.1+，无需额外依赖。
- 脚本行为：镜像同步——所有账号 `experts.json` 始终等于文件夹实际清单，覆盖前自动备份。

## 输出要求

- 诊断结论先汇报：哪些账号是来源、哪些待同步、哪些注册表含悬空条目，再执行写入。
- 每一步改动前后均告知用户备份位置与受影响的账号（以 `<账号UUID>` 指代，不输出真实账号信息）。
- 同步与部署完成后给出验证结果清单；未成功项给出原因与建议动作。
- 边界声明：本技能仅对本机生效，换电脑需在该机器重新执行；只同步注册表，不迁移专家包实体（前提是包已存在于共享的本地 marketplace 中）。
