---
name: weixin-reader
description: 提取微信公众号文章内容，支持任意公众号文章链接的内容抓取和结构化输出。
triggers:
  - "微信公众号"
  - "mp.weixin.qq.com"
  - "微信文章"
allowed-tools: ["Bash", "Read", "Write"]
---

# 微信公众号阅读器

提取微信公众号文章内容，支持任意公众号文章链接的内容抓取。

## 使用方法

直接发送微信公众号文章链接即可：
- https://mp.weixin.qq.com/s/xxxx

## 功能

- 自动渲染 JavaScript 动态内容
- 提取标题、作者、公众号名称、发布时间、正文内容
- 输出干净的 Markdown 格式
- **SSRF 防护**：DNS 解析验证，防止访问内网地址

## 依赖

- Python 3.8+
- Playwright
- playwright-stealth（反爬增强，可选）
- dnspython（DNS 解析安全校验）

安装依赖：
```bash
cd ~/.openclaw/workspace/skills/weixin-reader
pip install -r requirements.txt
playwright install chromium
```

## 安全说明

### SSRF 防护
- 禁止访问 localhost、127.0.0.1 等本地地址
- 禁止访问 10.x.x.x、172.16-31.x.x、192.168.x.x 等私有网段
- **DNS 解析检查**：验证域名解析后的 IP 不是内网地址（防止 DNS 重绑定攻击）

### 使用限制
- 仅支持提取公开文章内容
- 请遵守目标网站的服务条款
- 不建议用于高频批量抓取

## 文件说明

- `extract.py` - 主提取脚本（推荐，标准模式）
- `extract_stealth.py` - 反爬增强模式（**可选**，使用 playwright-stealth，可能违反某些网站 ToS）
- `extract_generic.py` - 通用网页提取

## 更新日志

### v1.1.0
- **结构化数据输出**：返回 JSON 格式，包含 metadata、content、stats 三个部分
- **新增统计信息**：字数、段落数、图片数、预估阅读时间
- **增强元数据**：提取时间戳、文章描述、HTML 内容
- **图片信息丰富**：返回图片 URL 和 alt 文本

### v1.0.1
- 增强 SSRF 防护：添加 DNS 解析验证
- 补充完整依赖：playwright-stealth, dnspython
- 完善安全说明文档