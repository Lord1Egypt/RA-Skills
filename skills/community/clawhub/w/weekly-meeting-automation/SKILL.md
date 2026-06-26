# 周例会自动化（Excel + 美信群发送）

## 概述

每周一早晨 9:00 自动处理周沟通事项跟进表，并将文件发送到美信工作群。适用于智能制造研究院智能装备所的周例会场景。

## 功能

| 功能 | 说明 |
|------|------|
| **自动找最新文件** | 从 `D:\00OPENCLAWSPACE\` 自动搜索 `装备所 周沟通事项跟进表 - *.xlsx`，按修改时间取最新（排除当天文件） |
| **日期替换** | 文件名中的日期（YYMMDD）自动替换为当天日期 |
| **Excel 操作** | 插入 B 列，填写当天日期 |
| **文件发送** | 通过 mx-im skill 上传文件并发送到指定美信群 |

## 文件清单

| 文件 | 路径 | 说明 |
|------|------|------|
| Excel 处理脚本 | `scripts/weekly_meeting_excel_process.ps1` | 自动找文件 + 日期替换 + Excel 操作 |
| 文件发送脚本 | `_send_meeting_excel.bat` | 通过 mx-im 发送文件到美信群（GBK 编码） |
| Cron 任务 | OpenClaw cron | 每周一 09:00 触发 |

## Cron 任务配置

```json
{
  "name": "每周一周例会Excel处理任务",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 1",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "每周一周例会 Excel 处理 + 发送到美信工作群。..."
  },
  "delivery": {
    "mode": "announce",
    "channel": "last"
  }
}
```

## 发送目标

| 项目 | 值 |
|------|-----|
| 群名 | (内)智能装备所工作群 |
| 群ID | 202410211824178783917 |
| 发送方式 | mx-im im_send.py (sub-type 7 文件消息) |

## 执行流程

```
周一 09:00 cron 触发
  ↓
Step 1: 运行 weekly_meeting_excel_process.ps1
  - 搜索 D:\00OPENCLAWSPACE\装备所 周沟通事项跟进表 - *.xlsx
  - 排除当天日期的文件
  - 按修改时间取最新
  - 复制为新文件，日期替换为当天
  - Excel 插入 B 列，填写日期
  ↓
Step 2: 解析脚本输出
  - [SUCCESS] → 提取文件路径
  - [ERROR] → 报告错误并停止
  ↓
Step 3: 运行 _send_meeting_excel.bat "<文件路径>"
  - UA 授权
  - 文件预上传 + ACK
  - 发送到美信群
  ↓
Step 4: 报告结果（推送到聊天）
```

## 依赖

| 依赖 | 说明 |
|------|------|
| **Excel** | Windows 本地 Excel/Office COM 组件 |
| **mx-im skill** | 美信消息发送脚本（ua_login.py + im_send.py） |
| **美信账号权限** | 需要开通文件上传和群消息发送功能 |

## 常见问题

### 错误码 30001
```
[ERROR] 预上传失败：{'code': 30001, 'msg': '该服务未授权，用户未开启对应功能配置'}
```
**解决**：在美信管理后台或账号设置中开启"外部应用发消息"和"文件上传"功能。

### PowerShell 空 body 参数丢失
```
im_send.py: error: argument --body: expected one argument
```
**解决**：文件发送使用 bat 脚本（GBK 编码 + chcp 936），不要用 PowerShell 直接调用。

### 自己覆盖自己
```
[ERROR] 无法使用项 XXX 其自身覆盖该项
```
**解决**：脚本已排除当天日期的文件，确保不会用今天的文件覆盖今天的新文件。

## 本地存档路径

- `D:\00OPENCLAWSPACE\_send_meeting_excel.bat`
- `scripts/weekly_meeting_excel_process.ps1`
