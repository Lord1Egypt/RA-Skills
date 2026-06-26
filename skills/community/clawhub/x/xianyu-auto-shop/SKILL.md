---
name: xianyu-auto-shop
displayName: 闲鱼全自动店铺托管
description: 自动擦亮宝贝、定时优化标题、私信自动回复、真人随机延迟、防风控防限流
version: 1.0.0
author: Claw运营助手
tags: [闲鱼,自动化,店铺托管,自动擦亮,自动回复]
user-invocable: true
metadata:
  openclaw:
    permissions: [accessibility, notification, auto-task]
---

# 闲鱼全自动店铺托管
## 功能介绍
1. 每日早晚高峰自动批量擦亮宝贝
2. 模拟真人操作 1.2–3.5秒随机延迟
3. 自带防风控规则，不连点、不高频操作
4. 私信智能自动回复接单话术
5. 每周自动优化商品标题提升搜索曝光

## 使用命令
批量擦亮
xianyu-auto-shop polish --max 40 --delay 2

自动回复挂机
xianyu-auto-shop reply start

标题优化
xianyu-auto-shop seo

## 推荐定时
每天 08:30、20:00 自动擦亮
每周一 09:00 自动优化标题
常驻监听私信自动回复
