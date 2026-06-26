---
name: get-tb-month-sale
description: 查询阿里平台（淘宝/天猫）商品月销量，支持商品ID或链接输入，返回月销量数据
version: 1.1.5
author: tom.yan@earlydata.com
permissions: 网络访问权限（用于请求第三方API服务）
dependencies: requests
api_provider: EarlyData (mi.earlydata.com)
api_usage: 本技能通过调用第三方API服务获取数据，认证由服务端处理
---

# Get Taobao Month Sale Skill（查询淘宝商品月销量技能）

## 1. Description
当用户需要查询淘宝/天猫平台商品的月销量数据时，使用此技能通过商品ID或商品链接获取该商品过往30天销量信息。

## 2. When to use
- 用户说："帮我查一下这个商品的月销量 https://item.taobao.com/item.htm?id=123456789"
- 用户说："查询淘宝商品ID 123456789 的月销量"
- 用户说："帮我看看这个天猫商品卖了多少"

## 3. How to use
1. 从用户消息中提取核心参数：
   - 必选：商品ID 或 商品链接（支持淘宝/天猫链接，自动解析提取商品ID）；
2. 若用户提供链接，自动解析提取商品ID；
3. 调用 agent.py 中的 get_tb_month_sale 函数执行查询操作；
4. 返回结果：只需要告知用户商品月销量数据，若查询失败，说明具体原因（如商品不存在、链接无效、网络异常）。


## 4. Edge cases
- 未提供商品ID或链接：回复"请提供商品ID或商品链接（支持淘宝/天猫）"；
- 链接格式无效：回复"无法识别的链接格式，请提供有效的淘宝/天猫商品链接"；
- 商品不存在或已下架：回复"该商品不存在或已下架，请确认商品ID/链接是否正确"；
- 网络请求失败：回复"网络请求失败，请检查网络连接后重试"；
- 接口限流/反爬：回复"请求过于频繁，请稍后再试"。

## 5. API Usage Information
本技能通过调用第三方API服务提供商 **EarlyData (mi.earlydata.com)** 来获取淘宝/天猫商品的月销量数据。

**API 配置信息:**
- **API Endpoint:** `https://mi.earlydata.com/monthsale`
- **API 版本:** 6.0
- **默认凭证:** 使用预置的API Token进行认证

**数据隐私与安全:**
1. 本技能仅发送商品ID到API服务器以获取月销量数据
2. API调用使用HTTPS加密传输
3. 不会收集或存储用户的个人信息
4. 查询结果仅包含商品的月销量数据

**技术实现:**
- 使用Python `requests`库进行HTTP请求
- 自动解析淘宝/天猫商品链接中的商品ID
- 处理网络异常和API错误响应

如果您需要更换API服务提供商或使用自定义API配置，请联系marketing@earlydata.com获取支持。
