---
name: webfetch
description: 网页内容抓取工具。使用 webfetch CLI 抓取网页内容并转换为 Markdown、文本或 HTML 格式。触发场景：用户要求抓取网页、获取网页内容、网页转 Markdown、网页转文本、下载网页。
---

# webfetch

封装 `webfetch` 命令行工具，用于抓取网页内容并转换为多种格式。

## 核心能力

1. **网页抓取** - 获取指定 URL 的网页内容
2. **格式转换** - 支持 Markdown（默认）、纯文本、原始 HTML 三种输出格式
3. **代理支持** - 自动读取环境变量代理配置，支持手动指定代理
4. **文件保存** - 支持将抓取内容保存到指定文件

## 工作流程

### 🌐 抓取网页内容

当用户表达抓取网页、获取网页内容、网页转 Markdown 意图时，执行如下命令：

```
webfetch "https://example.com"
```

视需要也可以使用如下常见用法：

```
webfetch "https://example.com"                    # 默认输出 Markdown
webfetch "https://example.com" -f text            # 输出纯文本
webfetch "https://example.com" -f html            # 输出原始 HTML
webfetch "https://example.com" -o article.md      # 保存到文件
webfetch "https://example.com" -q > output.md     # 静默模式，适合管道
```

### 🔧 代理配置

当网络环境需要代理时，有两种方式：

**方式一：环境变量（推荐）**

```
export HTTPS_PROXY=http://proxy:8080
webfetch "https://example.com"
```

**方式二：命令行参数**

```
webfetch "https://example.com" --proxy http://proxy:8080
```

### 🔓 跳过证书验证

当遇到 TLS 证书问题（如自签名证书）时：

```
webfetch "https://example.com" --insecure
```

### ⏱️ 超时设置

当目标网站响应较慢时：

```
webfetch "https://example.com" --timeout 60
```

### 🛠️ 错误排查

如果执行失败，按照以下步骤排查：

```
1. 检查安装 → 2. 检查网络 → 3. 检查代理配置
```

**Step 1: 检查是否安装 webfetch**

```
command -v webfetch
```

如果未安装，执行：

```
npm install -g @lyhue1991/webfetch
```

**Step 2: 检查网络连接**

```
curl -I https://example.com
```

**Step 3: 检查代理配置**

```
printenv HTTP_PROXY HTTPS_PROXY
```

如果需要代理但未配置：
```
webfetch "https://example.com" --proxy http://proxy:8080
```

### 📄 不同输出格式

**Markdown 格式（默认）**

```
webfetch "https://mp.weixin.qq.com/s/xxx" -o article.md
```

**纯文本格式**
```
webfetch "https://example.com" -f text
```

**原始 HTML**

```
webfetch "https://example.com" -f html
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `<url>` | 目标 URL，必填 |
| `-f, --format <format>` | 输出格式：markdown（默认）、text、html |
| `-t, --timeout <seconds>` | 超时时间（秒），最大 120，默认 30 |
| `-o, --output <file>` | 保存到指定文件 |
| `-q, --quiet` | 静默模式，仅输出内容 |
| `--proxy <url>` | 代理服务器地址 |
| `--insecure` | 跳过 TLS 证书验证 |

## 环境变量

| 变量 | 说明 |
|------|------|
| `HTTP_PROXY` | HTTP 请求代理 |
| `HTTPS_PROXY` | HTTPS 请求代理 |
| `NO_PROXY` | 跳过代理的主机列表 |

## 注意事项

1. **优先用 Markdown** - Markdown 格式保留结构信息，适合阅读和后续处理
2. **代理证书问题** - 使用代理时如遇证书错误，添加 `--insecure` 参数
3. **响应大小限制** - 最大支持 5MB 响应内容
4. **JavaScript 渲染** - 不支持 JavaScript 渲染，仅抓取静态页面

## 退出码

| 代码 | 说明 |
|------|------|
| 0 | 成功 |
| 1 | 用户错误（无效 URL、参数错误） |
| 2 | 网络错误（超时、DNS 解析失败） |
| 3 | 服务器错误（4xx、5xx 响应） |

## 快速参考

```
# 查看帮助
webfetch --help

# 查看版本
webfetch --version

# 基础抓取
webfetch "https://example.com"

# 输出纯文本
webfetch "https://example.com" -f text

# 保存到文件
webfetch "https://example.com" -o output.md

# 使用代理
webfetch "https://example.com" --proxy http://proxy:8080

# 跳过证书验证
webfetch "https://example.com" --insecure

# 自定义超时
webfetch "https://example.com" --timeout 60

# 静默模式（适合管道）
webfetch "https://example.com" -q > output.md

```