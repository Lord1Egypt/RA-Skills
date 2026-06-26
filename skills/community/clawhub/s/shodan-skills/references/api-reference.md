# Shodan API 参考文档

## 目录
- [概览](#概览)
- [认证](#认证)
- [API 端点](#api-端点)
- [搜索语法](#搜索语法)
- [常见用例](#常见用例)
- [速率限制](#速率限制)

## 概览

Shodan 是一个物联网搜索引擎，用于发现连接到互联网的设备。通过 Shodan API，你可以：
- 查询特定 IP 地址的详细信息
- 按条件搜索设备
- 获取 DNS 信息
- 分析网络资产和安全隐患

## 认证

### API Key 获取
1. 访问 https://account.shodan.io/register 注册账号
2. 登录后访问 https://developer.shodan.io/api
3. 在页面顶部或账户设置中找到 API Key

### 使用方式
API Key 作为查询参数传递：
```
https://api.shodan.io/shodan/host/8.8.8.8?key={YOUR_API_KEY}
```

## API 端点

### 1. 主机信息查询

**端点**: `/shodan/host/{ip}`

**方法**: `GET`

**描述**: 查询指定 IP 地址的详细信息，包括开放端口、服务、地理位置等。

**参数**:
- `ip` (路径参数): IP 地址
- `history` (可选): 是否包含历史数据（true/false）
- `minify` (可选): 是否返回简化数据（true/false）

**响应示例**:
```json
{
  "ip_str": "8.8.8.8",
  "hostnames": ["dns.google"],
  "country_code": "US",
  "country_name": "United States",
  "city": "Mountain View",
  "org": "Google LLC",
  "isp": "Google LLC",
  "asn": "AS15169",
  "ports": [53, 443],
  "latitude": 37.751,
  "longitude": -97.822,
  "data": [
    {
      "port": 53,
      "transport": "udp",
      "service": "dns",
      "dns": {
        "recursive": true
      }
    }
  ]
}
```

### 2. 设备搜索

**端点**: `/shodan/host/search`

**方法**: `GET`

**描述**: 按条件搜索互联网连接的设备。

**参数**:
- `query` (必需): 搜索查询字符串
- `facets` (可选): 要返回的统计维度，用逗号分隔
- `page` (可选): 页码，从 1 开始，默认 1
- `minify` (可选): 是否返回简化数据（true/false）

**可用 Facets**:
- `asn`: 自治系统号
- `country`: 国家代码
- `city`: 城市
- `org`: 组织
- `isp`: ISP 名称
- `os`: 操作系统
- `port`: 端口号
- `product`: 产品名称
- `version`: 版本号

**响应示例**:
```json
{
  "total": 1234567,
  "matches": [
    {
      "ip_str": "1.2.3.4",
      "port": 80,
      "org": "Example Corp",
      "location": {
        "country_code": "US",
        "city": "New York"
      }
    }
  ],
  "facets": {
    "country": [
      {"value": "US", "count": 500000},
      {"value": "CN", "count": 300000}
    ]
  }
}
```

### 3. 统计结果数量

**端点**: `/shodan/host/count`

**方法**: `GET`

**描述**: 统计匹配查询的设备数量，不返回具体设备信息。

**参数**:
- `query` (必需): 搜索查询字符串
- `facets` (可选): 要返回的统计维度

**响应示例**:
```json
{
  "total": 1234567,
  "facets": {
    "country": [
      {"value": "US", "count": 500000}
    ]
  }
}
```

### 4. DNS 域名查询

**端点**: `/dns/domain/{domain}`

**方法**: `GET`

**描述**: 查询指定域名的 DNS 记录。

**参数**:
- `domain` (路径参数): 域名

**响应示例**:
```json
{
  "domain": "google.com",
  "dns_records": {
    "A": ["172.217.164.110"],
    "MX": ["alt1.aspmx.l.google.com"],
    "NS": ["ns1.google.com"],
    "TXT": ["v=spf1 include:_spf.google.com ~all"]
  }
}
```

### 5. 反向 DNS 查询

**端点**: `/dns/reverse/{ip}`

**方法**: `GET`

**描述**: 查询指向指定 IP 的域名。

**参数**:
- `ip` (路径参数): IP 地址

**响应示例**:
```json
{
  "8.8.8.8": ["dns.google"]
}
```

### 6. 端口列表

**端点**: `/shodan/ports`

**方法**: `GET`

**描述**: 获取 Shodan 爬取的所有端口列表。

**响应示例**:
```json
[21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995]
```

### 7. 搜索查询列表

**端点**: `/shodan/query`

**方法**: `GET`

**描述**: 获取社区分享的搜索查询列表。

**参数**:
- `page` (可选): 页码，默认 1
- `sort` (可选): 排序字段（votes, timestamp）
- `order` (可选): 排序方向（asc, desc）

**响应示例**:
```json
{
  "total": 1000,
  "matches": [
    {
      "title": "Vulnerable Webcams",
      "query": "webcam has_screenshot:true",
      "votes": 50,
      "tags": ["webcam", "security"]
    }
  ]
}
```

### 8. 获取当前 IP

**端点**: `/tools/myip`

**方法**: `GET`

**描述**: 获取发起请求的 IP 地址。

**响应**: IP 地址字符串（纯文本）

### 9. 账户信息

**端点**: `/api-info`

**方法**: `GET`

**描述**: 获取 API 账户信息和使用情况。

**响应示例**:
```json
{
  "query_credits": 100,
  "scan_credits": 50,
  "monitored_ips": 10,
  "plan": "member"
}
```

## 搜索语法

### 基础搜索

**按端口搜索**:
```
port:80          # 开放 80 端口的设备
port:22,23,80    # 开放多个端口的设备
```

**按国家搜索**:
```
country:US       # 美国的设备
country:CN       # 中国的设备
country:DE       # 德国的设备
```

**按组织搜索**:
```
org:"Google"     # 属于 Google 的设备
org:"Amazon"     # 属于 Amazon 的设备
```

**按产品搜索**:
```
product:nginx    # 运行 nginx 的设备
product:Apache   # 运行 Apache 的设备
product:MySQL    # 运行 MySQL 的设备
```

**按操作系统搜索**:
```
os:Windows       # Windows 系统
os:Linux         # Linux 系统
os:Ubuntu        # Ubuntu 系统
```

### 高级搜索

**组合条件**:
```
port:80 country:US org:"Google"
# 查询美国 Google 开放 80 端口的设备

product:nginx os:Linux
# 查询运行 nginx 的 Linux 系统

port:22 -country:CN
# 查询开放 22 端口但不包括中国的设备（使用减号排除）
```

**范围搜索**:
```
port:1-100       # 端口范围 1-100
port:>1024       # 端口大于 1024
port:<1000       # 端口小于 1000
```

**网络范围**:
```
net:192.168.1.0/24    # 特定网段
ip:192.168.1.1        # 特定 IP
```

**地理位置**:
```
city:"New York"       # 特定城市
geo:40.71,-74.00      # 经纬度附近
```

**时间范围**:
```
before:2023-12-31     # 指定日期之前
after:2023-01-01      # 指定日期之后
```

### 特殊过滤器

**设备类型**:
```
webcam               # 网络摄像头
router               # 路由器
server               # 服务器
firewall             # 防火墙
printer              # 打印机
```

**安全相关**:
```
has_screenshot:true   # 有截图的设备
has_vuln:true         # 有漏洞的设备
vuln:CVE-2021-44228   # 特定 CVE 漏洞
```

**服务特征**:
```
http.title:"Welcome"       # HTTP 标题包含
http.component:jQuery      # 使用 jQuery
http.status:200            # HTTP 状态码
ssl.cert.issuer:Cisco      # SSL 证书颁发者
```

## 常见用例

### 1. 查找特定组织的暴露资产
```bash
search 'org:"Target Org"'
```

### 2. 查找暴露在互联网的数据库
```bash
search 'product:MySQL port:3306'
search 'product:MongoDB port:27017'
```

### 3. 查找特定漏洞的设备
```bash
search 'vuln:CVE-2021-44228'
search 'product:Apache vuln:CVE-2021-41773'
```

### 4. 查找物联网设备
```bash
search 'port:23 product:"Embedded Device"'
search 'webcam has_screenshot:true'
```

### 5. 网络安全审计
```bash
# 查找开放危险端口的设备
search 'port:3389,22,23,telnet'

# 查找使用过时协议的设备
search 'ssl.version:sslv2 OR ssl.version:sslv3'
```

## 速率限制

### 免费账户
- 每分钟 1 次请求
- 每月 100 次查询
- 无法使用监控功能

### 付费计划
- **Member**: 每月 $49
  - 每秒 1 次请求
  - 每月 5,000 次查询
  
- **Freelancer**: 每月 $19
  - 每秒 1 次请求
  - 每月 1,000 次查询

- **Enterprise**: 自定义
  - 无限制访问
  - 专属支持

### 最佳实践
1. 使用 `count` 接口先统计数量，再决定是否需要详细查询
2. 使用 `facets` 参数获取统计信息，减少数据传输量
3. 合理使用分页，避免一次性获取大量数据
4. 缓存查询结果，避免重复请求
