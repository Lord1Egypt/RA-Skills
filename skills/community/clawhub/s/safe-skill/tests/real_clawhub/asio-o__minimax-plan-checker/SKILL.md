---
name: minimax-plan-checker
description: 获取 MiniMax 平台的套餐信息，包括套餐名称、额度、当前使用情况。当用户询问 MiniMax 套餐、额度使用情况、API 调用量、计费信息时使用此技能。
---

# MiniMax 套餐信息查询

获取 MiniMax 平台的套餐名称、额度、当前使用情况。

## 使用方式

### 方式一：使用浏览器自动登录获取（推荐）

```bash
python C:\Users\YangF\.openclaw\workspace\skills\minimax-plan-checker\scripts\get_plan.py
```

### 方式二：在对话中直接使用

告诉用户需要打开浏览器，询问是否要自动打开 MiniMax 平台页面获取套餐信息。

## 输出格式

脚本会输出以下信息：
- **套餐名称**：如 "Chat API" / "MoE API" 等
- **额度信息**：总额度、已使用额度、剩余额度
- **使用统计**：API 调用次数、Token 使用量等

## 注意事项

- 需要用户已登录 MiniMax 账号
- 如果未登录，浏览器会打开登录页面，用户登录后再运行脚本
- 页面 URL: https://platform.minimaxi.com/user-center/payment/coding-plan
