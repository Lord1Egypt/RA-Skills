---
name: wechat-publisher
description: 微信公众号文章发布工具。从互联网获取信息，智能排版成精美文章，支持多格式输入，批量发布，定时发布，数据统计。自媒体运营必备工具。微信公众号、文章发布、自媒体。
version: 1.0.4
license: MIT-0
metadata: {"openclaw": {"emoji": "📱", "requires": {"bins": ["python3", "curl"], "env": ["WECHAT_APP_ID", "WECHAT_APP_SECRET"]}, "primaryEnv": "WECHAT_APP_ID"}}
dependencies: "pip install requests beautifulsoup4 markdown pillow pymupdf python-docx"
---

# 微信公众号文章发布工具

从互联网获取信息，智能排版成精美文章，一键发布到微信公众号。

## 功能特点

- 🌐 **智能获取**：从互联网获取最新信息
- 📝 **AI排版**：智能总结排版成精美文章
- 🎨 **多模板**：标准/营销/新闻等多种风格
- 🖼️ **AI生成图片**：集成china-image-gen，根据内容生成配图
- 📷 **图片嵌入**：支持内嵌图片和封面
- 📄 **多格式输入**：支持Word/PDF/Markdown
- 🌐 **网页抓取**：支持从网页URL提取内容
- 📦 **批量发布**：一次发布多篇文章
- ⏰ **定时发布**：支持定时发布功能
- 📊 **数据统计**：发布后查看阅读数据
- 🔄 **多公众号**：支持切换多个公众号

## ⚠️ 配置要求

> **需要微信公众号的AppID和AppSecret**
> 申请地址：https://mp.weixin.qq.com
> 需要开通"发布能力"权限

## 使用场景

```
"帮我把这篇Markdown发布到微信公众号"
"从这篇网页生成公众号文章并发布"
"帮我写一篇关于AI的公众号文章"
"批量发布这5篇文章到公众号"
"查看昨天文章的阅读数据"
```

---

## 配置方法

### 环境变量配置

```bash
# 设置微信公众号配置
export WECHAT_APP_ID='your_app_id'
export WECHAT_APP_SECRET='your_app_secret'
export WECHAT_AUTHOR='你的名字'
```

### 配置文件（可选）

```json
{
  "wechat": {
    "app_id": "your_app_id",
    "app_secret": "your_app_secret",
    "author": "Your Name"
  }
}
```

---

## 工作流程

```
用户输入（网页URL/Markdown/Word/PDF/简单描述）
        ↓
1. 内容获取
├─ 网页URL → OpenClaw web-search提取正文
├─ 简单描述 → OpenClaw AI模型扩展生成
├─ Markdown → 直接使用
├─ Word → 转换为Markdown
└─ PDF → 提取文本
        ↓
2. AI智能处理（OpenClaw大模型）
├─ 智能总结
├─ 优化排版
├─ 提取标题
├─ 生成摘要
└─ 优化语言表达
        ↓
3. 模板渲染
├─ 选择模板风格
├─ 渲染HTML
└─ 内嵌图片
        ↓
4. 发布到公众号
├─ 上传封面图
├─ 创建草稿
├─ 可选：直接发布
└─ 可选：定时发布
        ↓
5. 数据统计
└─ 查看阅读数据
```

### 信息来源

| 来源 | 说明 |
|------|------|
| **OpenClaw web-search** | 获取最新资讯、数据 |
| **OpenClaw AI模型** | 总结、优化、扩展内容 |
| **用户输入文件** | Word/PDF/Markdown |
| **用户输入URL** | 网页内容提取 |
| **china-image-gen** | AI生成配图 |

---

## Python代码

```python
import os
import requests
import json
import time

class WechatPublisher:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expires = 0
    
    def get_access_token(self):
        """获取access_token"""
        if self.access_token and time.time() < self.token_expires:
            return self.access_token
        
        url = f"https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if "access_token" in data:
            self.access_token = data["access_token"]
            self.token_expires = time.time() + data["expires_in"] - 300
            return self.access_token
        else:
            raise Exception(f"获取token失败: {data}")
    
    def create_draft(self, title, content, author="", thumb_media_id=""):
        """创建草稿"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
        
        payload = {
            "articles": [{
                "title": title,
                "author": author,
                "content": content,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 1
            }]
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if "media_id" in data:
            return data["media_id"]
        else:
            raise Exception(f"创建草稿失败: {data}")
    
    def publish(self, media_id):
        """发布文章"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={token}"
        
        payload = {"media_id": media_id}
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if "publish_id" in data:
            return data["publish_id"]
        else:
            raise Exception(f"发布失败: {data}")
    
    def get_publish_status(self, publish_id):
        """获取发布状态"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/get?access_token={token}"
        
        payload = {"publish_id": publish_id}
        
        response = requests.post(url, json=payload)
        return response.json()
    
    def get_article_data(self, article_id, begin_date, end_date):
        """获取文章数据统计"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/datacube/getarticleanalysis?access_token={token}"
        
        payload = {
            "begin_date": begin_date,
            "end_date": end_date,
            "msgid": article_id
        }
        
        response = requests.post(url, json=payload)
        return response.json()
    
    def list_drafts(self, offset=0, count=20):
        """获取草稿列表"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}"
        
        payload = {
            "offset": offset,
            "count": count,
            "no_content": 1
        }
        
        response = requests.post(url, json=payload)
        return response.json()
    
    def delete_draft(self, media_id):
        """删除草稿"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/delete?access_token={token}"
        
        payload = {"media_id": media_id}
        
        response = requests.post(url, json=payload)
        return response.json()
    
    def list_published(self, offset=0, count=20):
        """获取已发布文章列表"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/batchget?access_token={token}"
        
        payload = {
            "offset": offset,
            "count": count
        }
        
        response = requests.post(url, json=payload)
        return response.json()
    
    def delete_published(self, article_id):
        """删除已发布文章"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/delete?access_token={token}"
        
        payload = {"article_id": article_id}
        
        response = requests.post(url, json=payload)
        return response.json()
    
    def get_account_info(self):
        """获取公众号账号信息"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/account/getaccountinfo?access_token={token}"
        
        response = requests.post(url)
        return response.json()

# 使用示例
publisher = WechatPublisher(app_id, app_secret)

# 创建并发布
draft_id = publisher.create_draft("标题", "<p>内容</p>", "作者")
publish_id = publisher.publish(draft_id)

# 获取数据统计
data = publisher.get_article_data(article_id, "2026-03-01", "2026-03-31")

# 管理草稿
drafts = publisher.list_drafts()
publisher.delete_draft(media_id)

# 管理已发布文章
published = publisher.list_published()
publisher.delete_published(article_id)
```

---

## 文章模板

### 商务蓝（专业商务）

```
┌─────────────────────────────────────────────────────────┐
│  [深蓝渐变头部]                                          │
│                                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                         │
│  标题：大标题（居中，白色，加粗）                         │
│  副标题：副标题（浅蓝色，居中）                           │
│                                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                         │
│  正文内容（黑色，14pt）                                   │
│                                                         │
│  • 要点1                                                │
│  • 要点2                                                │
│  • 要点3                                                │
│                                                         │
│  [深蓝渐变底部]                                          │
│  作者：XXX | 来源：XXX                                   │
└─────────────────────────────────────────────────────────┘
```

### 极简白（清新简洁）

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  标题：大标题（左对齐，黑色，加粗）                       │
│  作者：XXX（灰色，小字）                                  │
│                                                         │
│  ─────────────────────────────────                      │
│                                                         │
│  正文内容（黑色，14pt）                                   │
│                                                         │
│  • 要点1                                                │
│  • 要点2                                                │
│  • 要点3                                                │
│                                                         │
│  ─────────────────────────────────                      │
│  来源：XXX                                              │
└─────────────────────────────────────────────────────────┘
```

### 暖色橙（生活分享）

```
┌─────────────────────────────────────────────────────────┐
│  [暖色渐变头部]                                          │
│                                                         │
│  标题：大标题（白色，居中）                               │
│  副标题：副标题（浅橙色）                                 │
│                                                         │
│  ─────────────────────────────────                      │
│                                                         │
│  正文内容                                                │
│                                                         │
│  • 要点1                                                │
│  • 要点2                                                │
│                                                         │
│  [暖色渐变底部]                                          │
│  作者：XXX                                              │
└─────────────────────────────────────────────────────────┘
```

### 科技绿（科技前沿）

```
┌─────────────────────────────────────────────────────────┐
│  [深绿渐变头部]                                          │
│                                                         │
│  标题：大标题（白色，加粗）                               │
│  副标题：副标题（浅绿色）                                 │
│                                                         │
│  ─────────────────────────────────                      │
│                                                         │
│  正文内容                                                │
│                                                         │
│  • 要点1                                                │
│  • 要点2                                                │
│                                                         │
│  [深绿渐变底部]                                          │
│  来源：XXX                                              │
└─────────────────────────────────────────────────────────┘
```

### 学术紫（学术研究）

```
┌─────────────────────────────────────────────────────────┐
│  [紫色渐变头部]                                          │
│                                                         │
│  标题：大标题（白色，居中）                               │
│  作者：XXX（浅紫色）                                     │
│                                                         │
│  ─────────────────────────────────                      │
│                                                         │
│  正文内容                                                │
│                                                         │
│  • 要点1                                                │
│  • 要点2                                                │
│                                                         │
│  [紫色渐变底部]                                          │
│  来源：XXX                                              │
└─────────────────────────────────────────────────────────┘
```
