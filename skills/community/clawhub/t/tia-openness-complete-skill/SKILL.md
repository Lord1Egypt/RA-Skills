---
name: tia-openness-complete-skill
description: 基于TIA Openness API的完整PLC自动化技能，支持项目创建、硬件配置、SCL编程、编译下载
author: jiansiting
version: 1.0.0
---

# TIA Openness 完整自动化技能

## 功能概述

本技能通过TIA Portal Openness API实现PLC工程的端到端自动化：

- 创建TIA Portal项目
- 添加PLC设备（支持S7-1200/1500）
- 根据工艺描述自动生成SCL程序块（OB/FC/FB/DB）
- 编译PLC软件
- 下载到PLC
- 支持单步操作和完整流程一键执行

## 环境要求

- Windows 10/11
- TIA Portal V16/V17/V18 已安装，并启用Openness组件
- Python 3.9+，已安装 `pythonnet` 和 `jinja2`
- 当前用户需属于 `Siemens TIA Openness` 用户组

## 安装依赖

```bash
pip install pythonnet jinja2