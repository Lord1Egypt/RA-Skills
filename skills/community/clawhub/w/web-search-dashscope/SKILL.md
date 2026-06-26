---
name: web-search-dashscope
description: 使用 Serper API 进行实时互联网搜索（国内可访问，基于 Google Search）
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["python"]
---

# Web Search 技能（Serper API 版本）

## 概述

此技能使用 **Serper API** 进行实时互联网搜索，基于 Google Search 结果。
- ✅ 国内可直接访问，无需梯子
- ✅ 免费额度：每月 2,500 次搜索
- ✅ 无需绑定信用卡

## 配置

### 1. 获取 API Key

1. 访问 Serper 官网：https://serper.dev/
2. 点击 **"Get API Key"** 或 **"Sign Up"**
3. 使用邮箱注册（支持 GitHub/Google 快捷登录）
4. 登录后在 **API Keys** 页面复制你的 API Key

### 2. 配置 API Key

编辑 `web_search.py` 文件，在顶部找到以下行：

```python
SERPER_API_KEY = "替换成你的 Serper API_KEY"
```

将 `替换成你的 Serper API_KEY` 替换为你实际的 API Key。

### 3. 安装依赖

确保已安装 Python requests 库：

```bash
pip install requests
```

## 使用方法

### 直接调用

```bash
python web_search.py "搜索关键词"
python web_search.py "今日天气" 5
```

### 在 OpenClaw 中使用

对 OpenClaw 说：
- "搜索今天的新闻"
- "搜索 AI 最新发展"
- "搜索北京天气"

## 免费额度与限制

- **免费额度**: 每月 2,500 次搜索
- **限流**: 每秒 1 次请求（1 QPS）
- **适用场景**: 实时新闻、天气、股票、金价、油价、技术文档等

## 技术细节

- **API 端点**: `https://google.serper.dev/search`
- **协议**: RESTful API
- **数据清洗**: 自动提取 title、snippet 和 link，避免 Token 浪费

## 故障排除

### 问题：返回 "请安装 requests 库"

**解决**: 运行 `pip install requests`

### 问题：返回 "网络错误"

**解决**: 检查网络连接，确认能访问外网

### 问题：返回 "未授权" 或 "API Key 无效"

**解决**: 检查 `web_search.py` 中的 API Key 是否正确填写

### 问题：搜索结果为空

**解决**: 尝试更换搜索关键词，或检查 API Key 额度是否用完
