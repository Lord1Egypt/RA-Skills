# 敏感信息检测 Skill

name: 错敏信息检测
description: 通过调用 UCAP 平台的安全防护接口，快速识别文本内容中的敏感数据。

## 简介

这是一个用于检测文本敏感信息的 Skill，通过调用 UCAP 平台的安全防护接口，快速识别文本内容中的敏感数据，适用于内容审核、数据合规等场景。

本技能支持从 URL 获取网页内容进行检测。

> ⚠️ **重要安全配置说明**
>
> **URL 抓取（静态模式 · 默认）**：
> - 默认使用静态模式：安全可靠，无需浏览器依赖
> - 使用 requests 抓取静态 HTML
>
> **⚠️ 动态模式需要显式启用**：
> - 设置 `DISABLE_JAVASCRIPT = False` 可开启动态模式
> - **必须配置 `ALLOWED_DOMAINS` 白名单**，否则动态模式直接拒绝访问
> - 页面 JS 可能发起内网请求（SSRF 风险），白名单是唯一防护手段
>
> **userKey 存储**：
> - 仅保存在当前进程环境变量，不持久化到磁盘
> - 如需长期使用，请在系统中配置持久化的 `UCAP_USERKEY` 环境变量

## 功能特性

- 支持多种敏感类型检测（可自定义检测类型列表）
- 支持从网页 URL 获取内容进行检测
- **静态模式（默认）**：使用 requests 抓取静态 HTML，安全高效，无需浏览器依赖
- **增强型 SSRF 防护**：DNS 解析 IP 检查、私有网段屏蔽、云元数据地址屏蔽、重定向二次校验
- **动态模式（可选）**：使用 agent-browser + Chrome 渲染 SPA（如需启用，请配置白名单）
- **强制 HTTPS**：默认仅允许 HTTPS 协议
- userKey 仅保存在当前进程，不持久化到磁盘
- 标准化的 JSON 格式输入输出
- 完善的错误处理和超时机制
- 兼容 OpenClaw 对话式调用

## 安全说明

### SSRF 防护（静态模式 / 默认）

| 防护层次 | 说明 |
|---------|------|
| 协议校验 | 默认仅允许 HTTPS，拒绝 http / ftp / file 等协议 |
| 主机名预检 | 拒绝直接以私有 IP 写入的 URL |
| **DNS 解析后 IP 检查** | 对域名进行 DNS 解析，检查所有 IP 是否为私有/保留网段 |
| 云元数据屏蔽 | 屏蔽 169.254.169.254、metadata.google.internal 等云平台元数据地址 |
| 重定向后校验 | 对页面最终落地 URL 重新执行完整安全检查 |

### ⚠️ 动态模式安全风险（需要显式启用 + 强制白名单）

**动态模式（`DISABLE_JAVASCRIPT = False`）需要同时满足两个条件才能使用**：
1. **显式启用**：代码中设置 `DISABLE_JAVASCRIPT = False`
2. **强制配置 `ALLOWED_DOMAINS` 白名单**：未配置则动态模式直接拒绝访问

不配置白名单的风险：

| 风险 | 说明 |
|------|------|
| 页面 JS 内网请求 | 恶意网页可能包含 `fetch("http://192.168.1.1/admin")` 等代码 |
| SSRF 绕过 | 虽然目标 URL 安全检查通过，但 JS 可能发起其他内网请求 |

**动态模式安全配置示例**：

```python
DISABLE_JAVASCRIPT = False  # ⚠️ 需要显式启用
ALLOWED_DOMAINS = [
    "news.example.com",
    "blog.trusted-site.cn",
    "*.github.io",
]
```

### 受屏蔽的私有/保留 IP 网段

| 网段 | 说明 |
|------|------|
| 10.0.0.0/8 | RFC1918 私有地址 |
| 172.16.0.0/12 | RFC1918 私有地址 |
| 192.168.0.0/16 | RFC1918 私有地址 |
| 127.0.0.0/8 | Loopback |
| 169.254.0.0/16 | Link-local / AWS 元数据 |
| 100.64.0.0/10 | RFC6598 共享地址 |
| 0.0.0.0/8 、240.0.0.0/4 等 | 保留地址 |
| ::1/128、fc00::/7、fe80::/10 | IPv6 私有/链路本地 |

### 域名白名单配置（动态模式强制要求）

**⚠️ 动态模式必须配置白名单，静态模式无需配置**

```python
# 动态模式：必须配置白名单（否则无法使用动态模式）
DISABLE_JAVASCRIPT = False
ALLOWED_DOMAINS = [
    "example.com",
    "*.trusted-domain.com",
]

# 静态模式（默认）：无需配置，保持 ALLOWED_DOMAINS = [] 即可
# 注意：智能模式（DISABLE_JAVASCRIPT=False）在静态模式失败时，
# 如果未配置白名单，将不会切换到动态模式，而是返回错误
```

### JavaScript 执行控制

```python
# 默认 True：仅使用静态模式
# - 始终使用 requests 抓取静态 HTML
# - 安全高效，无需浏览器依赖
# - 适合大多数网页内容抓取
DISABLE_JAVASCRIPT = True

# 设为 False：智能模式
# - 先尝试静态模式（requests），安全高效
# - 静态抓取失败或内容为空时，自动切换动态模式（agent-browser）
# - ⚠️ 动态模式需要配置 ALLOWED_DOMAINS 白名单！
DISABLE_JAVASCRIPT = False
```

### SSL/TLS 安全

- 默认启用 SSL 证书验证
- 遇到证书问题时返回友好错误提示

## 技术实现

### 使用的技术栈

| 技术 | 用途 |
|------|------|
| Python 3.8+ | 主要开发语言 |
| requests | HTTP 请求库（静态模式 / API 调用） |
| beautifulsoup4 | HTML 解析（静态模式下提取标题） |
| dnspython | DNS 解析（SSRF 防护） |

### 依赖安装

```bash
pip install -r requirements.txt
```

或单独安装：

```bash
pip install requests>=2.31.0
pip install dnspython>=2.4.0
pip install beautifulsoup4>=4.12.0
```

### ⚠️ 动态模式附加依赖

如需启用动态模式（`DISABLE_JAVASCRIPT = False`），还需安装：

| 依赖 | 安装命令 | 说明 |
|------|---------|------|
| Node.js | - | agent-browser 运行的基础环境 |
| agent-browser | `npm install -g agent-browser` | 命令行浏览器控制工具 |
| Chrome/Firefox | - | agent-browser 自动控制，需提前安装 |

**⚠️ 注意**：动态模式需要额外的系统依赖（Node.js + agent-browser + Chrome），且必须配置 `ALLOWED_DOMAINS` 白名单。

## 使用方法

### 对话式调用

```
请帮我检测这段文本是否包含敏感信息：{待检测文本内容}
```

或从 URL 检测：

```
请帮我检测这个网页的内容：https://example.com
```

### userKey 配置

**userKey 为可选参数**：

| 配置方式 | 体验限制 | 说明 |
|---------|---------|------|
| 不传入 userKey | 体验用户，每周 **10 次** 调用 | 无需注册 |
| 传入 userKey | 无调用限制 | 需前往 UCAP 平台申请 |

**⚠️ userKey 存储说明**：
- 仅保存在当前进程环境变量，**不会持久化到磁盘**
- 进程结束后自动失效
- 如需长期使用，请在系统中配置持久化的 `UCAP_USERKEY` 环境变量
- 新会话首次使用需重新传入 userKey

```
# 示例 1：体验使用（无需密钥，每周 10 次）
请帮我检测这段文本是否包含敏感信息：{待检测文本}

# 示例 2：传入 userKey（解除调用限制）
请帮我检测并设置密钥：您的userKey
```

如需更换密钥，重新传入新的 userKey 即可覆盖。

### 参数说明

| 参数名 | 类型 | 必传 | 说明 |
|--------|------|------|------|
| content | string | 是 | 待检测的文本内容 或 URL |
| userKey | string | 否 | UCAP 平台用户密钥（可选，不传则为体验用户；仅保存在当前进程） |
| sensitive_code_list | array | 否 | 检测类型列表，不传则检测所有类型 |

### 返回格式

```json
{
  "code": 0,
  "message": "检测成功",
  "data": {
    // UCAP 接口返回的检测结果
  },
  "source_url": "https://example.com",
  "source_type": "url"
}
```

### 错误码说明

#### 通用错误码
| 错误码 | 说明 |
|--------|------|
| 0 | 检测成功 |
| -1 | 待检测文本不能为空 |

#### API 调用错误
| 错误码 | 说明 |
|--------|------|
| -3 | 接口调用超时（15秒） |
| -4 | 接口返回错误 |
| -5 | 网络连接失败 |
| -6 | 接口调用失败 |
| -7 | 接口返回非 JSON 格式数据 |
| -8 | SSL 证书验证失败 |

#### URL 访问错误
| 错误码 | 说明 |
|--------|------|
| -100 | URL 安全检查失败（私有 IP / DNS 重绑定 / 非白名单域名 / 重定向后不安全 / 动态模式未配置白名单） |
| -101 | 访问超时 |
| -103 | agent-browser 错误（仅动态模式，需要确保已安装） |
| -104 | 访问失败（其他错误） |

## 示例代码

```python
from main import check_sensitive, fetch_url_content, run, validate_url_security

# 安全校验（不实际抓取）
ok, msg = validate_url_security("https://example.com")
print(ok, msg)

# URL 抓取（静态模式，默认行为）
result = fetch_url_content("https://example.com")

# 传入 userKey（解除体验限制）
result = check_sensitive(
    content="这是一段待检测的文本内容",
    userKey="your_user_key_here"
)

# 自动识别 URL 或文本
result = run({
    "content": "这是一段待检测的文本内容",
    "userKey": "your_user_key_here"
})
```

## 注意事项

1. 使用前需要获取有效的 UCAP 平台 userKey（可选，体验用户每周 10 次）
2. 接口调用超时时间为 15 秒
3. 网页加载超时时间为 30 秒
4. 所有 URL 请求均经过 SSRF 安全校验
5. **默认使用静态模式**：安全高效，无需浏览器依赖
6. 如需启用动态模式，设置 `DISABLE_JAVASCRIPT = False` **并配置 `ALLOWED_DOMAINS` 白名单**
7. **userKey 仅保存在当前进程**，不会持久化到磁盘

## 申请 userKey

访问 https://safeguard.ucap.com.cn/ 申请专属 userKey
