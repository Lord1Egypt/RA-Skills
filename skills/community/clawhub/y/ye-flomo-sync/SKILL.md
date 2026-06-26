---
name: flomo-sync
description: 快速同步内容到flomo笔记，支持自动标签识别、内容格式化。使用当用户提到：同步到flomo、存到flomo、发送到flomo、flomo记录、记到flomo、#flomo 等关键词时触发。
---

# flomo-sync Skill

## 配置要求
flomo Webhook地址需存储在 `~/.flomo_token` 文件中，修改地址直接更新该文件即可。

## 使用方法
1. 直接说要记录的内容，自动发送到flomo
2. 内容中包含的 `#标签` 会被flomo自动识别分类
3. 支持纯文本、链接、任意内容片段格式

## 调用脚本
使用 `scripts/flomo.sh <内容>` 执行同步操作，返回成功/失败结果。
