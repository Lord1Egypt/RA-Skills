---
name: workspace-health
displayName: 工作目录健康检测
description: 检测并修复OpenClaw工作目录嵌套问题
version: 1.0.0
type: skill
tags: [openclaw, workspace, health, directory, nested]
release: published
---

检测并修复OpenClaw工作目录嵌套问题。

## 触发条件

用户提到以下任意关键词时激活：
- 工作目录异常
- 嵌套目录
- .openclawworkspace
- workspace问题
- 路径错误
- openclaw doctor
- openclaw init

## 功能

### 1. 检测嵌套目录
扫描 `.openclawworkspace` 递归嵌套目录

### 2. 校验工作目录
- 检查配置文件中的工作目录
- 检查当前工作目录
- 验证路径有效性

### 3. 修复功能
- 删除嵌套目录
- 修复配置文件中的工作目录路径

## 使用方法

```powershell
# 检测嵌套目录
.\detect-nested-workspace.ps1

# 校验工作目录
.\validate-workspace.ps1

# 修复（演练模式）
.\fix-nested-workspace.ps1 -DryRun:$true

# 修复（执行）
.\fix-nested-workspace.ps1 -DryRun:$false
```

## 脚本位置

- `E:\.openclaw\workspace\scripts\detect-nested-workspace.ps1`
- `E:\.openclaw\workspace\scripts\validate-workspace.ps1`
- `E:\.openclaw\workspace\scripts\fix-nested-workspace.ps1`

## 注意事项

- 修复前建议先运行演练模式
- 确保配置文件有备份
- 修复后需要重启OpenClaw Gateway
