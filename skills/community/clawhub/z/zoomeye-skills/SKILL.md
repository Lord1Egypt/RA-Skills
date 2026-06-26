---
name: zoomeye
description: ZoomEye 网络空间搜索引擎集成，支持资产搜索、主机发现、Web应用探测；当用户需要进行网络资产测绘、漏洞资产发现、端口扫描结果查询或威胁情报分析时使用
metadata: {"openclaw":{"emoji":"🔍","requires":{"env":["ZOOMEYE_API_KEY"]},"primaryEnv":"ZOOMEYE_API_KEY"}}
dependency:
  python:
    - requests==2.31.0
---

# ZoomEye 网络空间搜索引擎

## 任务目标
- 本 Skill 用于：集成 ZoomEye API，实现网络空间资产搜索与分析
- 能力包含：用户信息查询、主机资产搜索、Web应用搜索、资源统计
- 触发条件：用户需要查询网络资产、进行安全评估、资产测绘或威胁情报分析

## 前置准备
- 依赖说明：scripts 脚本所需的依赖包
  ```
  requests==2.31.0
  ```
- 凭证配置：需要 ZoomEye API Key
  - 获取方式：访问 https://www.zoomeye.org/pricing?aff=INVITE-4KZ6-640E 注册账号后，在个人中心获取 API Key

## 操作步骤

### 1. 用户信息查询
- **用途**：查询当前 API Key 的用户信息、配额余额
- **执行方式**：调用 `scripts/zoomeye_api.py` 的用户信息查询功能
- **命令示例**：
  ```bash
  python scripts/zoomeye_api.py --action user-info
  ```
- **输出内容**：用户名、积分余额、VIP等级、配额信息

### 2. 主机资产搜索
- **用途**：搜索互联网上的主机资产，支持多种查询语法
- **执行方式**：调用 `scripts/zoomeye_api.py` 的主机搜索功能
- **命令示例**：
  ```bash
  python scripts/zoomeye_api.py --action host-search --query "port:80" --facets "app,os"
  ```
- **查询语法**（常用）：
  - `port:80` - 搜索指定端口
  - `ip:1.1.1.1` - 搜索指定 IP
  - `app:nginx` - 搜索指定应用
  - `os:linux` - 搜索指定操作系统
  - `country:cn` - 搜索指定国家
  - `city:beijing` - 搜索指定城市
  - 组合查询：`port:80 AND app:nginx`
- **输出内容**：IP、端口、服务、操作系统、地理位置、域名等

### 3. Web应用搜索
- **用途**：搜索互联网上的 Web 应用、网站、Web 服务
- **执行方式**：调用 `scripts/zoomeye_api.py` 的 Web 搜索功能
- **命令示例**：
  ```bash
  python scripts/zoomeye_api.py --action web-search --query "app:wordpress" --facets "webapp"
  ```
- **查询语法**：
  - `app:wordpress` - 搜索指定 Web 应用
  - `title:index` - 搜索网页标题
  - `keywords:login` - 搜索网页关键词
  - `headers:server` - 搜索 HTTP 响应头
- **输出内容**：网站标题、域名、IP、Web应用、响应头、网站指纹等

### 4. 资源统计
- **用途**：获取搜索结果的统计数据，而非详细数据
- **执行方式**：调用 `scripts/zoomeye_api.py` 的统计功能
- **命令示例**：
  ```bash
  python scripts/zoomeye_api.py --action stats --query "port:80" --facet "app"
  ```
- **输出内容**：按指定字段统计的数量分布

## 资源索引
- **API 脚本**：见 [scripts/zoomeye_api.py](scripts/zoomeye_api.py)
  - 功能：ZoomEye API 封装
  - 参数：action（操作类型）、query（查询语句）、facets（聚合字段）、page（分页）
- **查询语法参考**：见 [references/query_syntax.md](references/query_syntax.md)
  - 内容：完整的 ZoomEye 查询语法说明

## 注意事项
- **配额限制**：ZoomEye API 有查询次数限制，建议先查询用户信息了解剩余配额
- **查询精度**：使用精确的查询语法可以提高搜索效率和准确性
- **结果分析**：搜索结果由智能体进行分析和解读，提供安全建议
- **分页处理**：大量结果需要分页查询，每页默认 20 条记录

## 使用示例

### 示例 1：查询用户配额
```bash
python scripts/zoomeye_api.py --action user-info
```

### 示例 2：搜索暴露在互联网上的 Redis 服务
```bash
python scripts/zoomeye_api.py --action host-search --query "port:6379 AND app:redis"
```

### 示例 3：搜索特定国家的 Web 应用
```bash
python scripts/zoomeye_api.py --action web-search --query "country:us AND app:nginx"
```

### 示例 4：统计全球开放 443 端口的服务分布
```bash
python scripts/zoomeye_api.py --action stats --query "port:443" --facet "app"
```
