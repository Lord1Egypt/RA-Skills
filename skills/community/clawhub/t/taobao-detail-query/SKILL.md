---
name: get-tb-detail
description: 查询阿里平台（淘宝/天猫）商品详情，支持商品ID或链接输入，返回详情数据
version: 1.0.5
author: tom.yan@earlydata.com
permissions: 网络访问权限（用于请求第三方API服务）
dependencies: requests
api_provider: EarlyData (mi.earlydata.com)
api_usage: 本技能通过调用第三方API服务获取数据，认证由服务端处理
---

# Get Taobao Product Detail Info Skill（查询淘宝商品详情技能）

## 1. Description
当用户需要查询淘宝/天猫平台商品的详情数据时，使用此技能通过商品ID或商品链接获取商品信息。

## 2. When to use
- 用户说："帮我查一下这个商品的详情 https://item.taobao.com/item.htm?id=123456789"
- 用户说："查询淘宝商品ID 123456789 的详情"
- 用户说："帮我看看这个天猫商品的详细信息"

## 3. How to use
1. 从用户消息中提取核心参数：
   - 必选：商品ID 或 商品链接（支持淘宝/天猫链接，自动解析提取商品ID）；
2. 若用户提供链接，自动解析提取商品ID；
3. 调用 agent.py 中的 get_tb_detail 函数执行查询操作；
4. 返回结果：告知用户商品详情数据以markdown形式展示，若查询失败，说明具体原因（如商品不存在、链接无效、网络异常）。

