---
name: wechat-article
description: 抓取微信公众号文章内容。当用户发送微信公众号文章链接（mp.weixin.qq.com）时自动触发，将文章内容提取为可读文本。无需API密钥。
---

# 微信公众号文章抓取

## 触发条件

用户消息中包含 `mp.weixin.qq.com` 链接时，自动使用此技能抓取文章内容。

## 使用方法

```bash
curl -s "https://down.mptext.top/api/public/v1/download?url=<URL_ENCODED_LINK>&format=markdown"
```

### 参数

| 参数 | 说明 |
|------|------|
| url | 文章链接（需URL编码） |
| format | 输出格式：html / markdown / text / json（默认html） |

## 步骤

1. 从用户消息中提取微信文章链接
2. 对链接进行 URL 编码
3. 调用接口抓取内容（推荐 markdown 格式）
4. 提取正文，去除 CSS、导航等噪音
5. 为用户生成文章摘要或回答用户关于文章的问题

## 注意事项

- 此接口无需 API 密钥
- 部分文章可能有字数限制或反爬处理
- 图片链接可能有时效性
- 如抓取失败，可尝试换 format 为 text
