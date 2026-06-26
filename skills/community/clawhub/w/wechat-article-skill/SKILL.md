---
name: wechat-article-fetcher
description: |
  微信公众号文章链接处理。当用户发送微信公众号文章链接时，自动获取并提取文章内容。
  触发条件：(1) 用户发送 http(s)://mp.weixin.qq.com/s/ 开头的链接 (2) 用户请求获取公众号文章内容
---

# 微信公众号文章获取

## 识别公众号链接

公众号文章链接特征：
- 域名: `mp.weixin.qq.com`
- 路径: `/s/` 开头
- 示例: `https://mp.weixin.qq.com/s/abc123def456`

## 获取文章内容的方法

> ⚠️ 微信服务器会检测请求头，必须携带正常浏览器的 User-Agent，否则返回 403。

### Agent 调用顺序（重要）

1. **优先使用 get_content.py 脚本** —— 稳定、无头、输出直接供模型消费。
2. **仅在脚本失败时改用 browser 工具** —— 脚本 stderr 会输出「建议 Agent 改用 browser 工具」等提示，此时再考虑浏览器。

### 方法一：get_content.py 脚本（首选）

本地 CLI，urllib + certifi + 真实 UA，自带重试（最多 3 次）。失败时 stderr 提示是否改用 browser。

```bash
# 安装依赖（首次）
pip install -r requirements.txt

# 调用
python scripts/get_content.py --url "https://mp.weixin.qq.com/s/xxx"
```

- 成功：正文输出到 stdout。
- 失败：stderr 输出原因及「建议 Agent 改用 browser 工具」。

### 方法二： browser 工具（脚本失败时的回退）

仅在脚本返回非 0 且 stderr 建议改用 browser 时使用：

```python
browser(action="navigate", url="用户发送的链接")
browser(action="snapshot")
```

## 内容提取要点

公众号页面结构：
- 文章正文在 `#page-content` 元素中
- 标题通常在 `#activity-name` 或 `h1` 标签
- 作者信息在 `.account_nickname` 或类似元素
- 发布时间需要从页面元数据提取

## 处理流程

1. **识别链接** → 检测到 `mp.weixin.qq.com/s/` 链接
2. **获取内容** → 调用 `get_content.py --url <链接>`
3. **成功** → 正文在 stdout，直接供模型消费
4. **失败** → 检查 stderr，若建议改用 browser，再用 browser 工具重试

## 注意事项

- 公众号文章可能需要登录才能完整抓取
- 部分文章有访问时间限制
- 图片可能需要单独处理（使用微信图床域名）
- **必须使用正常浏览器的 User-Agent**
