---
name: shodan-skills
description: 查询 Shodan 物联网搜索引擎获取设备信息、安全数据和网络资产；当用户需要进行 IP 地址分析、设备搜索、DNS 查询、网络安全评估或获取物联网设备信息时使用
metadata: {"openclaw":{"emoji":"🔍","requires":{"env":["SHODAN_API_KEY"]},"primaryEnv":"SHODAN_API_KEY"}}
dependency:
  python:
    - requests==2.28.0
---

# Shodan API Skill

## 任务目标
- 本 Skill 用于：通过 Shodan API 查询互联网连接设备信息、进行网络安全分析
- 能力包含：主机信息查询、设备搜索、DNS 解析、反向 DNS 查询、端口扫描结果获取
- 触发条件：用户提到 IP 地址查询、设备搜索、网络安全分析、物联网设备、端口扫描、DNS 查询等

## 前置准备
- 依赖说明：
  ```
  requests==2.28.0
  ```
- API Key 配置：需预先配置 Shodan API Key（通过 skill_credentials 工具完成）

## 操作步骤

### 1. 主机信息查询
当用户提供 IP 地址时，查询该 IP 的详细信息：

**调用脚本**：
```bash
python scripts/shodan_api.py host <ip>
```

**示例**：
```bash
python scripts/shodan_api.py host 8.8.8.8
```

**返回信息包含**：
- 地理位置信息（国家、城市、经纬度）
- 组织和 ISP 信息
- 开放端口列表
- 服务和协议详情
- 安全标签和漏洞信息
- 主机名和域名

### 2. 设备搜索
当用户需要按条件搜索设备时：

**调用脚本**：
```bash
python scripts/shodan_api.py search "<query>" [--facets <facets>] [--page <page>]
```

**常用搜索语法**（详见 references/api-reference.md）：
- `port:80` - 搜索开放 80 端口的设备
- `country:US` - 搜索美国的设备
- `product:nginx` - 搜索运行 nginx 的设备
- `os:Windows` - 搜索 Windows 系统
- `org:"Google"` - 搜索属于 Google 的设备

**示例**：
```bash
# 搜索开放 80 端口的 Web 服务器
python scripts/shodan_api.py search "port:80"

# 搜索运行 Apache 的设备，显示国家和组织信息
python scripts/shodan_api.py search "product:Apache" --facets "country,org"

# 分页查询
python scripts/shodan_api.py search "port:22" --page 2
```

### 3. 统计结果数量
当用户只想知道匹配设备数量时：

**调用脚本**：
```bash
python scripts/shodan_api.py count "<query>" [--facets <facets>]
```

**示例**：
```bash
# 统计开放 80 端口的设备数量
python scripts/shodan_api.py count "port:80"

# 按国家统计
python scripts/shodan_api.py count "port:80" --facets "country"
```

### 4. DNS 查询
当用户需要查询域名相关的 DNS 信息：

**正向 DNS 查询**：
```bash
python scripts/shodan_api.py dns-domain <domain>
```

**反向 DNS 查询**：
```bash
python scripts/shodan_api.py dns-reverse <ip>
```

**示例**：
```bash
# 查询 google.com 的 DNS 信息
python scripts/shodan_api.py dns-domain google.com

# 反向查询 8.8.8.8 的域名
python scripts/shodan_api.py dns-reverse 8.8.8.8
```

### 5. 其他实用功能

**获取端口列表**：
```bash
python scripts/shodan_api.py ports
```

**获取搜索查询列表**：
```bash
python scripts/shodan_api.py queries [--page <page>] [--sort <sort>] [--order <order>]
```

**获取当前 IP**：
```bash
python scripts/shodan_api.py myip
```

**获取账户信息**：
```bash
python scripts/shodan_api.py profile
```

### 6. 数据分析与报告（智能体处理）
获取 API 数据后，智能体将：
- 分析返回的设备信息、安全数据和网络资产
- 识别潜在的安全风险和漏洞
- 生成结构化的安全评估报告
- 提供安全建议和最佳实践

## 资源索引
- API 脚本：见 [scripts/shodan_api.py](scripts/shodan_api.py)（统一 API 调用工具）
- API 参考：见 [references/api-reference.md](references/api-reference.md)（完整的 API 文档、搜索语法和参数说明）

## 注意事项
- Shodan API 有查询限制，免费账户每分钟 1 次请求，付费账户有更高配额
- 使用 `count` 接口可以节省查询配额
- 搜索查询语法详见 references/api-reference.md
- API Key 从环境变量 `SHODAN_API_KEY` 自动读取，无需手动传递
- 所有 API 调用会自动处理鉴权和错误响应

## 使用示例

### 示例 1：分析特定 IP 的安全状态
**用户请求**："帮我分析 8.8.8.8 的安全信息"
**执行步骤**：
1. 调用脚本获取主机信息
2. 智能体分析开放端口、服务版本、地理位置
3. 生成安全评估报告

### 示例 2：搜索特定类型的设备
**用户请求**："查找所有暴露在互联网上的摄像头设备"
**执行步骤**：
1. 构建搜索查询：`webcam has_screenshot:true`
2. 调用 search 接口获取结果
3. 智能体分析并生成威胁报告

### 示例 3：资产发现
**用户请求**："帮我发现某个组织的互联网资产"
**执行步骤**：
1. 使用 `org:"组织名"` 搜索
2. 调用 count 接口统计资产分布
3. 智能体生成资产清单和风险评估
