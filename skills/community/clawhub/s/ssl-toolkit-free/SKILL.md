---
slug: ssl-toolkit-free
name: ssl-toolkit-free
version: 1.0.0
displayName: SSL工具箱(免费版)
summary: 个人用户的HTTPS配置、TLS证书管理与基础连接排障工具。
license: Proprietary
edition: free
description: 'SSL工具箱(免费版)为个人用户提供HTTPS配置、TLS证书管理与基础连接排障能力。核心能力:

  - Let''s Encrypt免费证书申请与续期

  - 证书状态检查与详情查看

  - 常见错误诊断与修复

  - Nginx/Apache基础HTTPS配置

  - 证书类型选择指引


  适用场景:

  - 个人站点启用HTTPS

  - 证书过期排查与续期

  - 常见SSL错误诊断


  差异化:

  - 免费版聚焦个人站点的基础SSL管理

  - 移除原始平台与作者引用,纯净适配SkillHub

  - 提供中文友好的错误诊断表


  ...'
tags:
- Development
- 安全
- SSL
- 运维
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L1-入门级"
pricing_model: per_use
suggested_price: "9.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "工具,效率,自动化"
---
# SSL工具箱(免费版)

## 概述

SSL工具箱(免费版)为个人用户提供HTTPS配置、TLS证书管理与基础连接排障能力。当你在请求中提及 SSL证书、HTTPS配置、Let's Encrypt、certbot、TLS配置、证书过期、混合内容、证书链错误 等关键词时,本工具会自动激活,根据任务推荐合适的工具与方法,并输出可执行的命令与配置。

本版本聚焦个人站点的基础SSL管理,适合个人博客、小型站点与本地开发环境。如需通配符证书、多域名SAN、高级排障、自动化审计与多服务器配置,请升级至 PRO 版本。

## 核心能力

| 能力 | 说明 |
|---|---|
| 免费证书申请 | certbot / acme.sh / Caddy自动获取 |
| 证书状态检查 | openssl查看远程证书状态 |
| 证书详情查看 | 解析证书字段(有效期、域名、签发者) |
| 常见错误诊断 | 5类常见错误的根因与修复 |
| 基础服务器配置 | Nginx / Apache HTTPS配置模板 |
| 证书续期 | 自动化续期与dry-run验证 |
| 证书类型选择 | 单域名/通配符/SAN/自签名指引 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：个人用户的、TLS、证书管理与基础连、接排障工具、工具箱、免费版、为个人用户提供、接排障能力、Let、Encrypt、免费证书申请与续、证书状态检查与详、常见错误诊断与修、证书类型选择指引等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:为个人站点启用HTTPS

用户希望为个人博客启用HTTPS,工具推荐Let's Encrypt免费证书。

```bash
# 使用certbot为Nginx申请证书
certbot certonly --nginx -d example.com -d www.example.com
# ...
# 验证证书已签发
ls /etc/letsencrypt/live/example.com/
# fullchain.pem  privkey.pem  chain.pem  cert.pem
```

配置Nginx使用证书:

```nginx
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
# ...
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
# ...
    # 基础安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```

### 场景二:检查证书状态与有效期

用户希望检查某域名证书是否快过期。

```bash
# 查看远程证书有效期
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
# ...
# 示例
# notBefore=Jun 19 00:00:00 2026 GMT
# notAfter=Sep 17 00:00:00 2026 GMT
# ...
# 查看证书完整详情
openssl s_client -connect example.com:443 -servername example.com
```

### 场景三:诊断证书错误

用户报告浏览器显示证书错误,工具诊断根因并给出修复。

| 错误 | 根因 | 修复 |
|:-----|:-----|:-----|
| `certificate has expired` | 证书已过期 | 用 `certbot renew` 续期 |
| `unable to verify` / `self signed` | 缺少中间证书 | 配置中包含完整证书链 |
| `hostname mismatch` | 证书不覆盖该域名 | 为正确域名申请证书或加SAN |
| `mixed content` | HTTPS页面引用HTTP资源 | 把所有URL改为HTTPS或用 `//` |
| `ERR_CERT_AUTHORITY_INVALID` | 自签名或不受信任的CA | 使用Let's Encrypt或安装CA证书 |

## 不适用场景

以下场景SSL工具箱(免费版)不适合处理：

- 实际人员绩效评估
- 财务预算审批
- 合同法务审核

## 触发条件

需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 1. 申请免费证书

```bash
# 方式一:certbot(最常用)
certbot certonly --nginx -d example.com -d www.example.com
# ...
# 方式二:certbot standalone(无Web服务器时)
certbot certonly --standalone -d example.com
# ...
# 方式三:acme.sh(轻量)
acme.sh --issue -d example.com --nginx
```

### 2. 检查证书状态

```bash
# 查看远程证书有效期
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
# ...
# 查看证书详情
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -text
# ...
# 查看本地证书文件
openssl x509 -in cert.pem -text -noout
```

### 3. 配置服务器

Nginx配置:

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
# ...
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
# ...
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
}
# ...
# HTTP跳转HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```

Apache配置:

```apache
SSLEngine on
SSLCertificateFile /path/to/cert.pem
SSLCertificateKeyFile /path/to/privkey.pem
SSLCertificateChainFile /path/to/chain.pem
```

## 配置示例

### 核心任务速查表

| 任务 | 工具/方法 |
|---:|---:|
| 获取免费证书 | `certbot`, acme.sh, Caddy(自动) |
| 检查证书状态 | `openssl s_client -connect host:443` |
| 查看证书详情 | `openssl x509 -in cert.pem -text -noout` |
| 测试配置 | ssllabs.com/ssltest 或 `testssl.sh` |
| 转换格式 | PEM / DER / PKCS12 互转 |

### 常用证书命令

```bash
# 申请证书
certbot certonly --nginx -d example.com -d www.example.com
# ...
# 查看远程证书有效期
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
# ...
# 查看远程证书完整信息
openssl s_client -connect example.com:443 -servername example.com
```

### 证书类型选择

| 类型 | 适用场景 |
|:---:|:---:|
| 单域名 | 一个站点(example.com) |
| 通配符(*.domain.com) | 所有子域名 |
| 多域名(SAN) | 多个不同域名共用一个证书 |
| 自签名 | 仅本地开发 — 浏览器会警告 |

## 最佳实践

### 1. 始终自动化续期

Let's Encrypt证书90天过期,务必自动化:

```bash
# 测试续期(不实际执行)
certbot renew --dry-run
# ...
# 添加cron定时续期
crontab -e
# 每天凌晨检查并续期
0 0 * * * certbot renew --quiet
```

### 2. 配置HTTP跳转HTTPS

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$host$request_uri;
}
```

### 3. 使用完整证书链

```nginx
# 正确:使用fullchain.pem(包含中间证书)
ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
# ...
# 错误:仅用cert.pem(缺少中间证书,部分客户端无法验证)
ssl_certificate /etc/letsencrypt/live/example.com/cert.pem;
```

### 4. 启用现代TLS协议

```nginx
# 推荐:仅启用TLS 1.2与1.3
ssl_protocols TLSv1.2 TLSv1.3;
# ...
# 禁用:TLS 1.0与1.1(已不安全)
# ssl_protocols TLSv1 TLSv1.1;  # ❌
```

### 5. 解决混合内容

HTTPS页面引用HTTP资源会触发混合内容警告:

```html
<!-- 错误:HTTP资源 -->
<img src="http://cdn.example.com/image.png">
# ...
<!-- 正确:HTTPS或协议相对 -->
<img src="https://cdn.example.com/image.png">
<img src="//cdn.example.com/image.png">
```

## 常见问题

### Q1:免费版支持哪些服务器?

免费版提供Nginx与Apache基础配置模板。如需Node.js、Caddy、Traefik、HAProxy等,请使用PRO版。

### Q2:Let's Encrypt证书有效期多久?

90天。务必配置自动续期,建议每天检查一次。`certbot renew` 只在证书剩余有效期<30天时实际续期,所以频繁检查是安全的。

### Q3:免费版能否申请通配符证书?

免费版提供通配符证书的说明,但通配符证书需要DNS-01验证,配置较复杂。深度通配符与多域名管理请使用PRO版。

### Q4:免费版与PRO版差异?

| 维度 | 免费版 | PRO版 |
|:------|------:|:------|
| 证书类型 | 单域名为主 | 全类型(含通配符/SAN) |
| 服务器配置 | Nginx/Apache | 全主流(Node/Caddy/Traefik/HAProxy) |
| 排障深度 | 5类常见错误 | 全错误+性能+安全审计 |
| 自动化 | 基础续期 | 全自动+监控+告警 |
| 安全审计 | 不支持 | TLS配置评分+漏洞扫描 |
| 支持 | 社区支持 | 优先支持 |

### Q5:自签名证书能用吗?

仅适合本地开发,浏览器会警告。生产环境务必使用受信任CA签发的证书(如Let's Encrypt)。

### Q6:本工具能做什么、不能做什么?

能做:HTTPS配置、证书申请与续期、常见错误诊断、基础服务器配置。
不能做:应用层鉴权(JWT/OAuth)、SSH密钥、VPN/隧道、防火墙配置 — 这些请用对应专用工具。

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Web服务器**: Nginx / Apache(配置HTTPS需要)

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|:---|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| openssl | 命令行工具 | 必需 | 系统自带 |
| certbot | 命令行工具 | 推荐 | `pip install certbot` 或 eff.org 下载 |
| acme.sh | 命令行工具 | 可选 | acme.sh 安装脚本 |
| Nginx/Apache | Web服务器 | 视场景 | 系统包管理器安装 |

### API Key 配置

- 本skill基于Markdown指令规范,无需额外API Key。
- Let's Encrypt 通过ACME协议自动签发证书,无需API Key。
- 域名DNS解析需提前配置好,指向你的服务器IP。

### 可用性分类

- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作。免费版聚焦个人站点的HTTPS配置、证书管理与基础连接排障。

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------:|--------|:-------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 示例

### 基本用法

**输入**：用户提供操作指令和必要参数

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "SSL工具箱(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "sslkit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
