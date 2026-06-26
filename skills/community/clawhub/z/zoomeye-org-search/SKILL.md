---
name: zoomeye-search
description: ZoomEye 网络空间搜索引擎 CLI（v3.0.0）。当用户想搜索网络资产（IP、设备、网站、服务）、查询 ZoomEye 数据、构建 ZoomEye dork 查询语句、或进行安全研究（资产测绘、漏洞影响面评估、暴露面发现）时使用。覆盖全部搜索语法——设备/OS/端口/协议、SSL证书、HTTP头/正文、地理位置、时间范围、指纹等。
---

# ZoomEye 网络空间搜索

通过 `zoomeye` CLI（v3.0.0）搜索全球网络资产。

## 何时使用

### 触发条件

当用户请求涉及以下任一情况时，**必须**加载本 skill：

- 搜索网络资产/设备/服务（"帮我搜一下...""查一下暴露的...")
- 构建 ZoomEye/Fofa/Shodan 类搜索引擎的 dork 查询语句
- **仅做语法转换**：用户描述了想搜什么但只想要 dork 语句，不执行搜索（"这个怎么搜""语法是什么""帮我把这句话转成 ZoomEye 语法"）
- 资产测绘、暴露面发现、漏洞影响面评估（需用 ZoomEye 执行搜索）
- 需要查询 ICP 备案、SSL 证书、HTTP 响应头等关联信息
- 用户明确提到 "zoomeye"、"ZoomEye"、"钟馗之眼"、"网络空间搜索"

### 不适用场景

- 用户只是在聊天中提到 ZoomEye 但不涉及实际操作
- 用户问的是其他搜索引擎（Shodan、Censys、Fofa），且没有说"用 ZoomEye 来搜"
- 纯理论讨论搜索语法，不需要执行

### 仅语法转换模式

如果用户只是想把自然语言转成 ZoomEye dork 语句（"这个怎么搜"、"帮我写个语法"、"转成 zoomeye 语句"），**不需要**检查环境和执行搜索，直接跳到 [工作流程 → 第1步：自然语言 → Dork 转换](#1-自然语言--dork-转换)，输出转换后的 dork 语句即可。

## 前置条件

### 第一步：检查环境

收到任何搜索请求后，**必须先**执行以下检查，不要假设环境已就绪：

```bash
# 检查是否已安装
which zoomeye && zoomeye -v

# 检查 token 是否已配置（init 后 token 持久化在 ~/.config/zoomeye/setting/，只需配置一次，后续会话无需重配）
zoomeye info
```

### 第二步：根据检查结果引导用户

**如果 `zoomeye` 未安装：**

提示用户安装：
```bash
pip3 install zoomeye
```

安装完成后继续下一步。

**如果 `zoomeye info` 返回 `login required, missing Authorization header`（未配置 token）：**

按以下步骤引导用户：

1. 告知用户需要 ZoomEye 的 API-KEY：
   > 使用 ZoomEye 搜索需要 API-KEY，请按以下步骤操作：
   > 1. 打开 https://www.zoomeye.org/profile 登录你的 ZoomEye 账号
   > 2. 在个人中心找到你的 API-KEY（不设过期时间，可随时重置）
   > 3. 把 API-KEY 发给我，我帮你执行初始化

2. 用户提供 KEY 后，执行：
   ```bash
   zoomeye init -apikey "<用户提供的APIKEY>"
   ```

3. 验证配置是否生效：
   ```bash
   zoomeye info
   ```
   确认返回的用户信息正确后，再开始搜索。

**如果 `zoomeye info` 正常返回用户信息：**

环境就绪，直接进入工作流程。

## CLI 命令一览

```bash
zoomeye -h                              # 帮助
zoomeye -v                              # 版本号
zoomeye info                            # 账户信息、订阅、积分余额
zoomeye search "<dork>" [参数]           # 核心搜索命令
zoomeye clear -cache                    # 清除本地缓存（~/.config/zoomeye/cache）
zoomeye clear -setting                  # 清除存储的 API Key 和 token
```

### search 命令参数

| 参数 | 说明 |
|------|------|
| `-page <n>` | 页码，默认第1页，按更新时间排序 |
| `-pagesize <n>` | 每页条数，默认10，最大10000 |
| `-sub_type {v4,v6,web,all}` | 数据类型。`v4`=IPv4设备（默认），`v6`=IPv6设备，`web`=网站/域名，`all`=全部 |
| `-facets <项目>` | 聚合统计，逗号分隔。支持：`country`、`subdivisions`、`city`、`product`、`service`、`device`、`os`、`port` |
| `-fields <字段列表>` | 返回字段，逗号分隔。默认：`ip,port,domain,update_time`。完整字段列表见 https://www.zoomeye.org/doc/ |
| `-figure {pie,hist}` | 数据可视化。必须与 `-facets` 配合使用 |
| `-save` | 将搜索结果保存为本地 JSON 文件 |
| `-force` | 忽略本地缓存，强制从 ZoomEye 实时获取 |

### 错误处理

| 错误信息 | 原因 | 处理 |
|---------|------|------|
| `login required, missing Authorization header` | 未配置 token | 执行 `zoomeye init -apikey "<APIKEY>"` |
| `rate limit exceeded` / 返回空数据 | 配额耗尽或频率限制 | 等待后重试，或检查账户积分 → `zoomeye info` |
| 命令执行超时 | 网络问题或 ZoomEye API 响应慢 | 重试一次，仍有问题提示用户检查网络 |

## 搜索语法

### 基本规则

- 搜索**不区分大小写**（仅 `==` 精准匹配时区分大小写）
- 搜索字符串会被**分词**后匹配（官网提供"分词"测试）
- 字符串值用引号包裹：`"Cisco System"` 或 `'Cisco System'`
- 字符串内引号用 `\` 转义：`"a\"b"`
- 括号用 `\` 转义：`portinfo\(\)`

### 逻辑运算符

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `=` | 模糊匹配（包含关键词） | `title="知道创宇"` |
| `==` | 精准匹配（区分大小写，可搜空值） | `title=="知道创宇"` |
| `\|\|` | 或 | `service="ssh" \|\| service="http"` |
| `&&` | 且 | `device="router" && after="2020-01-01"` |
| `!=` | 非 | `country="CN" && subdivisions!="beijing"` |
| `()` | 括号优先级 | `(country="CN" && port!=80) \|\| (country="US" && title!="404 Not Found")` |
| `*` | 模糊通配符 | `title="google*"` |

### 搜索字段速查

#### 设备与服务指纹

| 字段 | 说明 | 常用值 |
|------|------|--------|
| `app` | 应用/产品指纹 | `"Cisco ASA SSL VPN"`、`"GitLab"`、`"phpMyAdmin"` |
| `service` | 服务协议 | `"ssh"`、`"http"`、`"ftp"`、`"telnet"`、`"mysql"`、`"redis"`、`"rdp"`、`"smb"` |
| `device` | 设备类型 | `"router"`、`"switch"`、`"storage-misc"`、`"firewall"`、`"webcam"` |
| `os` | 操作系统 | `"RouterOS"`、`"Linux"`、`"Windows"`、`"IOS"`、`"JUNOS"` |
| `title` | HTML 标题 | `"admin"`、`"login"`、`"Cisco"` |
| `industry` | 行业类型 | `"政府"`、`"科技"`、`"能源"`、`"金融"`、`"制造业"` |
| `product` | 组件/产品名 | `"Cisco"`、`"Apache"`、`"Nginx"` |
| `protocol` | 传输协议 | `"TCP"`、`"UDP"`、`"TCP6"`、`"SCTP"` |
| `is_honeypot` | 是否蜜罐 | `"True"` / `"False"` |

#### IP、域名与组织

| 字段 | 说明 | 示例 |
|------|------|------|
| `ip` | IP 地址（v4/v6） | `ip="8.8.8.8"`、`ip="2600:3c00::f03c:91ff:fefc:574a"` |
| `cidr` | CIDR 网段 | `cidr="52.2.254.36/24"`（C段，/16=B段，/8=A段） |
| `org` / `organization` | 组织名称（中英文均可） | `org="北京大学"` |
| `isp` | 网络服务提供商 | `isp="China Mobile"` |
| `asn` | 自治系统编号 | `asn=42893` |
| `port` | 端口号 | `port=80`（暂不支持多端口） |
| `hostname` | IP 主机名 | `hostname="google.com"` |
| `domain` | 域名/子域名 | `domain="baidu.com"` |
| `icp.number` | ICP 备案号 | `icp.number="京ICP备10040895号-40"` |
| `icp.name` | ICP 备案企业名称 | `icp.name="知道创宇"` |

#### 地理位置

| 字段 | 说明 | 示例 |
|------|------|------|
| `country` | 国家（缩写/中英文） | `"CN"`、`"中国"`、`"US"` |
| `subdivisions` | 省/行政区（中英文） | `"beijing"`、`"北京"`、`"guangdong"` |
| `city` | 城市（中英文） | `"changsha"`、`"长沙"` |

#### SSL/TLS 证书

| 字段 | 说明 | 示例 |
|------|------|------|
| `ssl` | 证书内容含关键词（常用于产品/公司名搜索） | `ssl="google"` |
| `ssl.cert.fingerprint` | SHA1 指纹 | `ssl.cert.fingerprint="F3C98F223D82CC41CF83D94671CCC6C69873FABF"` |
| `ssl.chain_count` | 证书链数量 | `ssl.chain_count=3` |
| `ssl.cert.alg` | 签名算法 | `ssl.cert.alg="SHA256-RSA"` |
| `ssl.cert.issuer.cn` | 签发者 CN | `ssl.cert.issuer.cn="pbx.wildix.com"` |
| `ssl.cert.subject.cn` | 持有者 CN | `ssl.cert.subject.cn="example.com"` |
| `ssl.cert.pubkey.rsa.bits` | RSA 公钥位数 | `ssl.cert.pubkey.rsa.bits=2048` |
| `ssl.cert.pubkey.ecdsa.bits` | ECDSA 公钥位数 | `ssl.cert.pubkey.ecdsa.bits=256` |
| `ssl.cert.pubkey.type` | 公钥类型 | `ssl.cert.pubkey.type="RSA"` |
| `ssl.cert.serial` | 证书序列号 | `ssl.cert.serial="18460192207935675900910674501"` |
| `ssl.cipher.bits` | 加密套件位数 | `ssl.cipher.bits="128"` |
| `ssl.cipher.name` | 加密套件名称 | `ssl.cipher.name="TLS_AES_128_GCM_SHA256"` |
| `ssl.cipher.version` | 加密套件版本 | `ssl.cipher.version="TLSv1.3"` |
| `ssl.version` | SSL/TLS 版本 | `ssl.version="TLSv1.3"` |
| `ssl.jarm` | JARM 指纹 | `ssl.jarm="29d29d15d29d29d00029d29d29d29dea0f89a2e5fb09e4d8e099befed92cfa"` |
| `ssl.ja3s` | JA3S 指纹 | `ssl.ja3s=45094d08156d110d8ee97b204143db14` |

#### HTTP 头与正文

| 字段 | 说明 | 示例 |
|------|------|------|
| `http.header` | HTTP 响应头含关键词 | `http.header="http"` |
| `http.header_hash` | 响应头 MD5 | `http.header_hash="27f9973fe57298c3b63919259877a84d"` |
| `http.header.server` | Server 头值 | `http.header.server="Nginx"` |
| `http.header.version` | 服务版本号 | `http.header.version="1.2"` |
| `http.header.status_code` | HTTP 状态码 | `"200"`、`"302"`、`"404"`、`"500"` |
| `http.body` | HTML 正文含关键词 | `http.body="document"` |
| `http.body_hash` | HTML 正文 MD5 | `http.body_hash="84a18166fde3ee7e7c974b8d1e7e21b4"` |

#### 协议报文、哈希与时间

| 字段 | 说明 | 示例 |
|------|------|------|
| `banner` | 非 HTTP 协议报文 | `banner="FTP"` |
| `iconhash` | favicon 哈希（支持 MD5 或 mmh3） | `iconhash="f3418a443e7d841097c714d69ec4bcb8"`、`iconhash="1941681276"` |
| `filehash` | 上传文件解析哈希 | `filehash="0b5ce08db7fb8fffe4e14d05588d49d9"` |
| `dig` | DNS dig 解析结果 | `dig="baidu.com 220.181.38.148"` |
| `after` | 更新时间晚于 | `after="2020-01-01"`（需组合其他过滤条件） |
| `before` | 更新时间早于 | `before="2020-01-01"`（需组合其他过滤条件） |

## 工作流程（AI 决策树）

环境检查通过后，按以下步骤构建并执行搜索：

### 1. 自然语言 → Dork 转换

用户的自然语言描述中包含以下关键词时，映射到对应搜索字段：

#### 地理位置关键词

| 用户说法 | 字段 | 转换结果 |
|---------|------|---------|
| "中国"、"国内"、"CN" | `country` | `country="CN"` |
| "美国"、"US"、"国外" | `country` | `country="US"` |
| "日本"、"JP" | `country` | `country="JP"` |
| "北京"、"北京市" | `subdivisions` | `subdivisions="beijing"` 或 `subdivisions="北京"` |
| "上海"、"广东"等省份城市 | `subdivisions` 或 `city` | `subdivisions="guangdong"` / `city="changsha"` |
| 国家全名如"新加坡" | `country` | `country="Singapore"` |

#### 端口/服务关键词

| 用户说法 | 字段 | 转换结果 |
|---------|------|---------|
| "开了XX端口"、"XX端口"、"端口XX" | `port` | `port=80` |
| "ssh"、"SSH服务"、"ssh协议" | `service` | `service="ssh"` |
| "http"、"网站"、"web服务" | `service` | `service="http"` |
| "数据库"、"mysql"、"redis"、"mongodb" | `service` | `service="mysql"` / `service="redis"` |
| "远程桌面"、"RDP"、"3389" | `service` 或 `port` | `service="rdp"` / `port=3389` |
| "telnet"、"FTP"、"SMB" | `service` | `service="telnet"` / `service="ftp"` |
| "TCP"、"UDP" | `protocol` | `protocol="TCP"` |

#### 设备/系统关键词

| 用户说法 | 字段 | 转换结果 |
|---------|------|---------|
| "路由器"、"路由设备" | `device` | `device="router"` |
| "交换机" | `device` | `device="switch"` |
| "摄像头"、"网络摄像头" | `device` | `device="webcam"` |
| "防火墙" | `device` | `device="firewall"` |
| "Linux"、"linux系统"、"linux服务器" | `os` | `os="Linux"` |
| "Windows"、"windows系统"、"windows服务器" | `os` | `os="Windows"` |
| "思科"、"Cisco"、"思科设备" | `app` | `app="Cisco"` |

#### 资产/组织关键词

| 用户说法 | 字段 | 转换结果 |
|---------|------|---------|
| "XX大学的"、"XX公司的"、"XX机构的" | `org` | `org="北京大学"` |
| "某IP段"、"C段"、"B段"、"X.X.X.X/24" | `cidr` | `cidr="52.2.254.36/24"` |
| "某域名"、"XX.com"、"子域名" | `domain` | `domain="baidu.com"` |
| "某IP"、"IP是X.X.X.X" | `ip` | `ip="8.8.8.8"` |
| "XX运营商"、"移动"、"电信"、"联通" | `isp` | `isp="China Mobile"` |

#### Web 应用关键词

| 用户说法 | 字段 | 转换结果 |
|---------|------|---------|
| "标题包含XX"、"网页标题" | `title` | `title="admin"` |
| "nginx"、"apache"、"iis"、"服务器是XX" | `http.header.server` | `http.header.server="Nginx"` |
| "状态码200"、"404页面" | `http.header.status_code` | `http.header.status_code="200"` |
| "网页内容包含XX"、"页面里有XX" | `http.body` | `http.body="phpMyAdmin"` |
| "管理后台"、"登录页"、"admin" | `title` | `title="admin" \|\| title="login" \|\| title="管理"` |

#### 指纹/证书关键词

| 用户说法 | 字段 | 转换结果 |
|---------|------|---------|
| "证书里包含XX"、"XX的SSL证书" | `ssl` | `ssl="google"` |
| "XX签发的证书" | `ssl.cert.issuer.cn` | `ssl.cert.issuer.cn="Let's Encrypt"` |
| "相同图标的网站"、"favicon是XX" | `iconhash` | `iconhash="f3418a443e..."` |
| "蜜罐"、"排除蜜罐" | `is_honeypot` | `&& is_honeypot!="True"` |
| "备案号XX"、"ICP备案" | `icp.number` / `icp.name` | `icp.number="京ICP备..."` |

#### 时间/版本关键词

| 用户说法 | 字段 | 转换结果 |
|---------|------|---------|
| "今年"、"最近"、"2025年之后" | `after` | `after="2025-01-01"` |
| "XX年之前"、"去年之前" | `before` | `before="2024-01-01"` |
| "版本XX"、"XX版本" | `http.header.version` | `http.header.version="12.0"` |

#### 自然语言 → Dork 转换示例

| 用户自然语言 | 转换后的 Dork |
|------------|-------------|
| "搜一下中国的 SSH 服务" | `country="CN" && service="ssh"` |
| "中国开了3306端口的Linux服务器" | `country="CN" && port=3306 && os="Linux"` |
| "日本的路由器设备" | `country="JP" && device="router"` |
| "国内的 Nginx 网站，排除蜜罐" | `country="CN" && http.header.server="Nginx" && is_honeypot!="True"` |
| "北京的管理后台页面" | `(title="admin" \|\| title="login" \|\| title="管理") && subdivisions="beijing"` |
| "2025年之后出现的 GitLab 资产" | `app="GitLab" && after="2025-01-01"` |
| "Let's Encrypt 签发证书的中国资产" | `ssl.cert.issuer.cn="Let's Encrypt" && country="CN"` |
| "搜北京大学的所有资产" | `org="北京大学"` |
| "中国开了22或3389端口的资产" | `country="CN" && (port=22 \|\| port=3389)` |
| "中国的 Redis 或 MongoDB 数据库" | `country="CN" && (service="redis" \|\| service="mongodb")` |
| "搜 52.2.254.36 这个 C 段的 HTTP 服务" | `cidr="52.2.254.36/24" && service="http"` |
| "网页内容含 phpMyAdmin 的中国网站" | `http.body="phpMyAdmin" && country="CN"` |

### 2. 构建 Dork

按以下原则拼接：

- **限制范围** → `&&`：`country="CN" && service="redis" && os="Linux"`
- **扩展匹配** → `||`：`port=80 || port=443 || port=8080`
- **排除干扰** → `!=`：`country="CN" && subdivisions!="beijing"`
- **复杂条件** → `()`：`(country="CN" && port!=80) || (country="US" && title!="404 Not Found")`

### 3. 选择 sub_type

| 场景 | sub_type |
|------|----------|
| 搜 IoT、服务器、摄像头、工控设备等 IPv4 资产 | `v4`（默认） |
| 搜 IPv6 资产 | `v6` |
| 搜网站、Web 应用、域名 | `web` |
| 不确定或需要全量 | `all` |

### 4. 执行策略（配额优化）

遵循"试探→验证→导出"三步法：

```bash
# 第1步：小量试探，确认 dork 语法正确且有数据
zoomeye search "<dork>" -pagesize 10

# 第2步：用 facets 看数据分布（pagesize=1 最省配额）
zoomeye search "<dork>" -facets country,service,os,device -pagesize 1

# 第3步：确定方向后大批量导出
zoomeye search "<dork>" -pagesize 1000 -save
```

### 5. Shell 引号规则

| 场景 | 外层引号 | 写法 |
|------|---------|------|
| dork 只有 `field="value"` 格式，不含单引号 | **单引号** | `zoomeye search 'country="CN" && service="ssh"'` |
| dork 内需要写单引号字符 | **双引号** | `zoomeye search "title='Cisco System'"` |
| dork 内含 `&&`、`\|\|` 等 shell 特殊符号 | **单引号**（最安全） | `zoomeye search 'service="ssh" \|\| service="http"'` |
| dork 内含 HTML 代码片段（dork 值内含引号字符） | **单引号**。`\"` 在单引号内原样传给 zoomeye，由 zoomeye 将其解析为值内的引号字面量 | `zoomeye search '"<body style=\"margin:0;padding:0\"> <p align=\"center\">"'` |

**关键原则：外层优先用单引号。** 单引号内所有字符都是字面量，包括 `\`、`"`、`$`，不会发生 shell 扩展。仅当 dork 本身包含单引号字符（少见）时才换用双引号外层。

## 搜索结果解读

```text
$ zoomeye search 'telnet' -pagesize 5
ip                port      domain        update_time
134.xx.xx.129     1901      [unknown]     2025-02-06T15:45:20
134.xx.xx.138     1901      [unknown]     2025-02-06T15:45:19

total: 5/9976411                  ← 当前页条数 / 全数据集匹配总数
```

使用 `-facets` 时底部追加聚合 Top 10：

```text
 ----------------------------------------
 ZoomEye total data:9976411
 -------------product Top 10-------------
 product                            count
 MikroTik router config httpd       3326013
 Apache httpd                       2411293
```

## 常用搜索场景

### 资产发现与暴露面

```bash
# 某国暴露的数据库服务
zoomeye search 'country="CN" && (service="redis" || service="mysql" || service="mongodb" || service="elasticsearch")' -pagesize 10

# 某国暴露的远程管理服务
zoomeye search 'country="CN" && (service="rdp" || service="ssh" || service="telnet") && is_honeypot!="True"' -pagesize 10

# 某组织的 IP 资产
zoomeye search 'org="北京大学"' -pagesize 100
zoomeye search 'isp="China Mobile" && country="CN"' -pagesize 100
```

### Web 应用识别

```bash
# 通过 Server 头找 Web 服务
zoomeye search 'http.header.server="nginx" && country="CN" && http.header.status_code="200"' -sub_type web -pagesize 10

# 通过标题找管理后台
zoomeye search '(title="admin" || title="login" || title="管理") && country="CN"' -sub_type web -pagesize 10

# 通过 body 内容找特定应用
zoomeye search 'http.body="phpMyAdmin" && country="CN"' -sub_type web -pagesize 10
```

### SSL 证书关联

```bash
# 某公司证书关联的资产
zoomeye search 'ssl="google"' -pagesize 10
# 某域名的证书持有者
zoomeye search 'ssl.cert.subject.cn="example.com"' -pagesize 10
# Let's Encrypt 签发的证书（值内含单引号，外层必须用双引号，内层双引号需 \" 转义）
zoomeye search "ssl.cert.issuer.cn=\"Let's Encrypt\" && country=\"CN\"" -pagesize 10
```

### 漏洞影响面评估

```bash
# 某产品在全球/某国的分布（第一步：了解规模）
zoomeye search 'app="GitLab"' -facets country -pagesize 1

# 某产品特定版本
zoomeye search 'app="GitLab" && http.header.version="12.0"' -pagesize 100

# 时间范围内新出现的资产
zoomeye search 'app="Confluence" && after="2025-01-01"' -pagesize 100
```

### 指纹与图标搜索

```bash
# 通过 favicon 找同源网站
zoomeye search 'iconhash="f3418a443e7d841097c714d69ec4bcb8"' -sub_type web -pagesize 10

# 通过 JARM 指纹找同类服务
zoomeye search 'ssl.jarm="29d29d15d29d29d00029d29d29d29dea0f89a2e5fb09e4d8e099befed92cfa"' -pagesize 10
```

### 网段与 IP

```bash
# C 段资产
zoomeye search 'cidr="52.2.254.36/24"' -pagesize 100
# B 段 + 特定服务
zoomeye search 'cidr="52.2.254.36/16" && service="http"' -pagesize 100
# IP 精确搜索
zoomeye search 'ip="8.8.8.8"' -pagesize 10
```

## SDK 用法

```python
from zoomeye.sdk import ZoomEye

zm = ZoomEye(api_key="你的APIKEY")

# 查询账户信息
zm.userinfo()

# 搜索（完整参数）
result = zm.search(
    dork='country=cn',           # 搜索查询语句（必填）
    qbase64='',                  # base64 编码的查询（与 dork 二选一）
    page=1,                      # 页码，默认1
    pagesize=20,                 # 每页条数，默认20
    sub_type='all',              # v4 / v6 / web / all
    fields='ip,port,domain,os,app,title',
    facets='country,service'
)

# 返回格式:
# {'code': 60000, 'message': 'success', 'query': 'country=cn',
#  'total': 823268005, 'data': [{...}], 'facets': {}}
```

## 注意事项

| 事项 | 说明 |
|------|------|
| 配额 | 每次搜索消耗积分。先用 `-pagesize 1` + `-facets` 摸底，再大批量导出 |
| 缓存 | 结果缓存在 `~/.config/zoomeye/cache`，有效期5天。重复查询不扣配额。用 `-force` 绕过缓存 |
| 多端口 | `port` 字段暂不支持同时搜索多个开放端口的目标 |
| `before`/`after` | 时间过滤器不能单独使用，需与其他条件组合 |
| Shell 引号 | 整个 dork 必须用引号包裹。外层优先用单引号 |
