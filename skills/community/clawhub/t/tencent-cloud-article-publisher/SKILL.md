---
name: tencent-cloud-publish
description: "将文章自动发布到腾讯云开发者社区 (https://cloud.tencent.com/developer)。需要提供：标题、正文（Markdown 或纯文本）、Cookie 认证信息。支持直接发布（addArticle API），无需打开浏览器。"
emoji: 📝
effort: medium
context: inherit
---

# tencent-cloud-publish

将文章直接发布到腾讯云开发者社区。

---

## 已验证的 API

**发布端点**: `POST https://cloud.tencent.com/developer/api/article/addArticle`

**已确认成功响应的 payload**:
```json
{
  "title": "文章标题",
  "content": "<p>HTML 格式正文内容</p>",
  "plain": "纯文本正文（不含 HTML 标签）",
  "summary": "文章摘要（自动生成或用户输入）",
  "userSummary": "用户填写的摘要",
  "sourceType": 1,
  "isOriginal": true,
  "classifyIds": [149],
  "openComment": 1,
  "closeTextLink": 0
}
```

**成功响应**: `{"articleId":2650368,"status":0}`
→ 文章立即发布成功，status=0 表示发布成功

---

## 发布流程

### 1. 转换内容格式

如果用户提供 Markdown → 转换为 HTML：
```python
import re

def md_to_html(md_text):
    # 粗体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md_text)
    # 斜体
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    # 代码块
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    # 换行
    html = re.sub(r'\n', '<br/>', html)
    return f'<p>{html}</p>'
```

### 2. 直接调用 API

```python
import requests
import json

def publish_article(title, content_md, cookie_str):
    """直接发布文章到腾讯云开发者社区"""
    
    # 1. 转换格式
    content_html = md_to_html(content_md)
    plain_text = content_md  # 纯文本
    
    # 2. 构建摘要
    summary = content_md[:100] + '...' if len(content_md) > 100 else content_md
    
    # 3. API 调用
    url = "https://cloud.tencent.com/developer/api/article/addArticle"
    headers = {
        "Cookie": cookie_str,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Referer": "https://cloud.tencent.com/developer/article/write-new",
        "Origin": "https://cloud.tencent.com",
    }
    payload = {
        "title": title,
        "content": content_html,
        "plain": plain_text,
        "summary": summary,
        "userSummary": summary,
        "sourceType": 1,
        "isOriginal": True,
        "classifyIds": [149],  # 149 = 技术
        "openComment": 1,
        "closeTextLink": 0
    }
    
    resp = requests.post(url, headers=headers, json=payload, timeout=15)
    result = resp.json()
    
    if "articleId" in result:
        article_id = result["articleId"]
        article_url = f"https://cloud.tencent.com/developer/article/{article_id}"
        return {"success": True, "articleId": article_id, "url": article_url}
    else:
        return {"success": False, "error": result.get("msg", "Unknown error")}
```

### 3. 获取 Cookie

用户需要从浏览器 DevTools 获取：
1. 打开 https://cloud.tencent.com/developer 并登录
2. 按 F12 → Application → Cookies → cloud.tencent.com
3. 复制以下 Cookie 字段的值，用分号连接：
   - `skey`
   - `qcloud_uid`
   - `qcommunity_session`
   - `loginType`
   - `qcommunity_identify_id`
   - `tinyid`
   - `uin`（可选）

---

## 安全注意事项

1. **Cookie 仅存内存**：不写入任何文件，用完即弃
2. **skey 包含特殊字符**（`*`）：requests 库会自动处理，无需 URL 编码
3. **有效期**：Cookie 会过期，发布失败时提示用户刷新 Cookie
4. **频率限制**：每次发布间隔建议 > 10 秒

---

## 使用方式

用户说"帮我发布文章到腾讯云"时触发。收集：
1. Cookie（从飞书私密消息传递）
2. 文章标题
3. 文章正文（支持 Markdown）
4. 分类（可选，默认技术类）

返回发布结果 + 文章链接。
