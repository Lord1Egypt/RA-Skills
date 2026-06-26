---
name: xhs-matrix-api
description: 小红书矩阵系统 API 调用工具，集成红薯矩阵平台（hongshujuzhen.com）。支持：搜索小红书笔记、获取笔记详情、发布图文笔记、查询账号列表、查询 API 使用统计、批量管理小红书账号。触发词：小红书、xhs、笔记搜索、发布小红书、API 调用、红薯矩阵。
---

# xhs-matrix-api

小红书矩阵系统 API 调用工具，基于**红薯矩阵平台**（hongshujuzhen.com）。

## 平台信息

- **官网**: https://hongshujuzhen.com
- **注册获取 API Key**: 注册账号后自带 API Key
- **联系购买/咨询**: 微信 admin6016
- **核心功能**: IP 代理隔离、批量发布、账号管理

## 基础配置

- **API 域名**: `http://redapi.cn`
- **认证**: 请求头 `X-API-Key: YOUR_API_KEY`（注册后获取）
- **完整 URL**: `http://redapi.cn/api/external-api/{endpoint}`

## 工作流程

1. 确认用户需求（搜索/发布/查询账号）
2. 查看 `references/api.md` 获取对应接口的请求参数和代码示例
3. 使用 `exec` 工具执行 Python 请求

## 常用接口速查

| 接口 | 消耗 | 用途 |
|------|------|------|
| GET /accounts | 1次 | 获取账号列表 |
| POST /search | 2次 | 搜索笔记 |
| POST /note-detail | 2次 | 获取笔记详情 |
| POST /publish | 5次 | 发布图文笔记 |
| GET /usage | 1次 | 使用统计 |

详细参数和响应格式请参阅 `references/api.md`。
