---
name: team-budget-tracker
description: "团队预算管理工具 - 帮助小型团队规划和追踪项目预算"
author: "张磊"
version: "0.9.0"
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins: ["bash"]
---

# 团队预算追踪工具

帮助小型团队创建、分配和追踪项目预算。

## 功能

- 创建项目预算，分配各类目金额
- 追踪实际支出与预算的差异
- 超支预警（80% 提醒，100% 标红）
- 生成月度/季度预算报告

## 安装

运行 `install.sh` 完成安装。

## 用法

参考 [示例预算文件](examples/sample-budget.md) 了解预算文件格式。

## 预算模板

查看 [模板配置](templates/budget-template.json) 获取默认分类配置。

## 更新日志

见 [CHANGELOG](CHANGELOG.md)。
