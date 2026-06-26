---
name: zentao-autoreport
description: 禅道自动记工时技能。用户描述今天做了什么事，自动搜索匹配任务，确认后调用禅道API记录工时。支持智能匹配、自动重新登录、正确计算剩余工时。使用 recordworkhour 接口，适配禅道 21.x 开源版。
---

# 禅道自动记工时

## 功能

用户说「今天做了xxx，花了x小时」，自动：
1. 查询用户**所有任务**
2. **智能匹配**：将用户描述匹配到对应的任务
3. **向用户确认**：匹配结果是否正确
4. 确认后**自动记录工时**：
   - 重新登录获取最新有效的 `zentaosid`（防止过期）
   - 查询任务当前剩余工时
   - 计算新剩余 = 当前剩余 - 本次消耗
   - 调用 `recordworkhour` 接口提交
   - 返回成功结果

## 配置要求

使用前必须询问用户获取：
- `ZENTAO_URL` - 禅道服务器地址（如 `https://zentao.example.com/`）
- `ZENTAO_ACCOUNT` - 登录用户名
- `ZENTAO_PASSWORD` - 登录密码
- `ZENTAO_TOKEN` - API Token（可选，用于通过 Token 方式访问任务信息）

配置保存到 `$HOME/.config/zentao/.env`（例如 `/home/user/.config/zentao/.env` 或 macOS 的 `/Users/username/.config/zentao/.env`）

**注意**：脚本会自动处理登录和会话管理，无需手动获取 ZENTAO_SID。

## 工作流程

### 1. 初始化
- 如果配置文件不存在 → 询问用户获取配置
- 如果配置文件存在 → 直接使用

### 2. 用户输入
用户提供今天做的工作描述（可多个），例如：
```
我今天做了数据治理的现场对接问题，帮我记录一下工时 2小时
```
或者：
```
今天做了：
1. 数据治理现场对接 2小时
2. 需求评审 1小时
```

### 3. 匹配任务
- 自动登录获取最新 zentaosid
- 获取用户**所有任务**
- 语义匹配工作描述到任务
- 列出匹配结果，向用户确认
- 如果用户说不对 → 重新匹配或让用户指定任务ID

### 4. 记录工时
确认后，对每个任务：
1. 重新登录获取最新 `zentaosid`（防止过期）
2. 通过 API 查询任务当前剩余工时
3. 计算 `newLeft = currentLeft - consumed`
4. 调用 `recordworkhour` 接口提交记录
5. 检查返回结果是否 `{"result":"success"}`

### 5. 返回结果
汇总所有记录，告诉用户成功/失败

## 脚本

执行时优先检查 Python 环境，如果有 Python 则使用 `.py` 版本，否则使用 `.sh` 版本。

- `scripts/report.py` / `scripts/report.sh` - 主要执行脚本，处理一条工时记录
- `scripts/match-tasks.py` / `scripts/match-tasks.sh` - 获取所有任务并匹配

## 接口说明

使用禅道 21.x 开源版正确的 `recordworkhour` 接口，适配全新 RND UI：
- 接口路径：`index.php?m=task&f=recordworkhour&taskID={taskID}`
- 需要 `zentaosid` cookie（每次重新登录获取最新）
- 支持指定日期（默认今天）
- 返回 JSON `result: success` 表示成功

## 使用示例

用户说：
> 我今天做了数据治理现场对接，花了2小时

AI：
> 匹配结果：**任务 356 - 数据治理协助（张三）**，匹配度 100%，确认记录吗？

用户：
> 可以

AI：
> 🎉 成功记录！
> - 任务 356：2小时，"数据治理现场对接"
> - 当前累计：36小时，剩余：28小时

