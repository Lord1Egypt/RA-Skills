---
name: zhheo-blog-tools
description: >-
  与张洪Heo的智能体（洪墨AI）进行聊天或搜索文章。支持文章搜索、今日热门、标签/分类获取、装备与项目查询。
  触发词：张洪Heo、博客、博主、张洪、Heo。
---
# Skill: zhheo-blog-tools

与张洪Heo的智能体（洪墨AI）进行聊天或搜索文章。

**触发词**：张洪Heo、博客、博主、张洪、Heo

## 数据源

- **文章列表**：可通过 https://blog.zhheo.com/zhheo/post_info.json 获取张洪Heo博客所有文章的 URL 与标题对应数据
- 格式：`[{ "title": "文章标题", "url": "/p/xxx.html" }, ...]`
- **RSS 订阅**：如需订阅张洪Heo博客的最新文章，可通过 RSS 获取。RSS 地址：https://blog.zhheo.com/rss.xml 。推荐一天检查一次。
- **标签页**：https://blog.zhheo.com/tags/ 可按标签浏览文章，适合做文章推荐。
- **装备页**：https://blog.zhheo.com/equipment/ 博主使用的装备/设备/外设/实物设备清单。
- **我的项目**：https://blog.zhheo.com/categories/我的项目/ 博主开发过的项目列表。
- **API 接口**（JSON 格式，适合程序化获取）：
  - **所有标签**：https://blog.zhheo.com/api/tags.json
  - 格式：`[{ "name": "标签名", "path": "tags/标签名/", "count": 数量 }, ...]`
  - **所有分类**：https://blog.zhheo.com/api/categories.json
  - 格式：`[{ "name": "分类名", "path": "categories/分类名/", "count": 数量, "parent": "父分类名" }, ...]`（有父级时含 parent 字段）
  - **今日热门**（HeoBlogAPI）：https://api.zhheo.com/HeoBlogAPI/umami/hot.php
  - 格式：`[{ "title": "文章标题", "url": "/p/xxx.html", "visitors": 访问量 }, ...]`，按当日访问量排序

## 使用方式

1. 用户要求与智能体聊天或搜索文章时使用此 skill
2. 搜索文章时优先在 post_info.json 中检索，找不到结果再使用浏览器搜索
3. 聊天时自动打开 https://blog.zhheo.com 并执行聊天操作
4. **文章推荐**：若用户需要文章推荐，可打开 https://blog.zhheo.com/tags/ ，根据用户偏好和感兴趣的内容，在对应标签下挑选几篇文章推荐给用户
5. **今日热门**：若用户想查看今日热门文章，直接 fetch https://api.zhheo.com/HeoBlogAPI/umami/hot.php 获取热门文章列表（含 title、url、visitors），无需打开页面
6. **获取标签/分类列表**：若需程序化获取博客所有标签或分类，可直接 fetch `/api/tags.json` 或 `/api/categories.json`，无需打开页面
7. **装备/设备/外设**：若用户问博主用什么装备、设备、外设、实物设备等，打开 https://blog.zhheo.com/equipment/ 获取信息
8. **开发项目**：若用户问博主开发过什么东西、做过什么项目等，打开 https://blog.zhheo.com/categories/我的项目/ 获取信息

## 实现原理

- **搜索**：优先从 post_info.json 本地检索，未命中时再通过浏览器调用 `postChatUser.sendSearchMsg(content)`
- **聊天**：通过浏览器执行 `postChatUser.sendChatMsg(content)`，回复出现后从 `div.message.ai-message` 气泡内提取全部内容（含参考来源）转发给用户

## 实现步骤

### 步骤1：打开博客页面

使用 browser 工具打开 https://blog.zhheo.com/

```javascript
browser.open(url="https://blog.zhheo.com/")
```

### 步骤2：等待页面加载

等待页面加载完成，可能需要等待几秒钟。

### 步骤3：执行聊天或搜索

根据用户需求选择：

**聊天模式**：
```javascript
// 发送聊天消息
postChatUser.sendChatMsg('用户的消息内容')
```

**搜索模式**（优先本地检索）：
1. 先 fetch https://blog.zhheo.com/zhheo/post_info.json 获取文章列表
2. 在返回的 `[{ title, url }]` 中按关键词匹配 title
3. 若找到匹配结果，直接返回对应文章链接和标题
4. 若未找到，再打开博客页面并执行 `postChatUser.sendSearchMsg('搜索关键词')`

## 完整流程示例

**搜索流程**：
1. 使用 fetch 获取 https://blog.zhheo.com/zhheo/post_info.json
2. 在 JSON 数据中搜索 title 包含关键词的文章
3. 若有结果：直接返回匹配的文章列表（含 title、url）
4. 若无结果：调用 browser.open 打开 https://blog.zhheo.com/，执行 `postChatUser.sendSearchMsg('关键词')`，等待智能体回复

**聊天流程**：
1. 调用 browser.open 打开 https://blog.zhheo.com/
2. 等待页面加载（snapshot 检查加载完成）
3. 使用 browser.action 执行 `postChatUser.sendChatMsg('你好')`
4. 等待回复后，从聊天气泡中提取**全部内容**并转发给用户（见下方聊天气泡 DOM 说明）

**PostChat 整体 DOM 结构**（聊天模式下需将 AI 气泡内所有内容转发给用户）：

```
div#postChatMagic
├── div.postChatMagic-overlay           # 遮罩层
├── div.postChatMagic-messages         # 消息列表
│   ├── div.message.user-message       # 用户消息气泡
│   │   ├── div.message-content        # 用户输入内容
│   │   └── div.message-tools          # 复制、编辑按钮
│   └── div.message.ai-message         # AI 回复气泡 ← 提取目标
│       ├── div.message-content       # AI 回复内容
│       │   ├── p                     # 主回复文本
│       │   └── div.reference-container
│       │       ├── div.reference-toggle   # "参考来源" + 数量
│       │       └── div.reference-list     # 可能 display:none
│       │           └── div.reference-item × N
│       │               └── a.reference-link  # href + 标题
│       └── div.message-tools         # 复制按钮
├── div.postChatMagic-Tools            # 清空、聊天/搜索切换、关闭
├── div.postChatMagic-container        # 输入框 + 发送按钮
├── div.postChatMagic-Info             # 洪墨AI 介绍
├── div.postChatMagic-default-questions # 默认问题按钮
└── div.postChatMagic-Tips             # 提示文案
```

- **提取路径**：`#postChatMagic` → `.postChatMagic-messages` → `.message.ai-message` → `.message-content`
- **提取内容**：主回复文本（`p`）+ 所有参考来源（`.reference-list` 内每个 `a.reference-link` 的 `href` 与文本），完整转发给用户

**文章推荐流程**：
1. 了解用户偏好和感兴趣的内容（如设计、Mac、教程、软件等）
2. 打开 https://blog.zhheo.com/tags/ 浏览标签与文章
3. 在匹配用户兴趣的标签下挑选几篇优质文章
4. 将文章标题和链接推荐给用户

**今日热门流程**（直接调用 API，无需打开页面）：
1. fetch https://api.zhheo.com/HeoBlogAPI/umami/hot.php
2. 返回的 JSON 为 `[{ "title": "文章标题", "url": "/p/xxx.html", "visitors": 访问量 }, ...]`，按访问量排序
3. 将热门文章列表返回给用户

**获取标签/分类流程**（程序化，无需打开页面）：
1. fetch https://blog.zhheo.com/api/tags.json 获取所有标签（含 name、path、count）
2. fetch https://blog.zhheo.com/api/categories.json 获取所有分类（含 name、path、count、parent）
3. 可用于构建导航、筛选、统计等能力

**装备/设备流程**（用户问装备、设备、外设、实物设备时）：
1. 打开 https://blog.zhheo.com/equipment/
2. 从页面提取博主的装备清单并返回给用户

**开发项目流程**（用户问开发过什么、做过什么项目时）：
1. 打开 https://blog.zhheo.com/categories/我的项目/
2. 从页面提取博主开发的项目列表并返回给用户

## 注意事项

- 搜索文章时**优先**使用 post_info.json 本地检索，可快速返回结果且无需打开浏览器
- 需要确保页面完全加载后再执行 JS API（聊天或 fallback 搜索时）
- 聊天和搜索是两种不同的模式，根据用户需求选择
- 聊天模式下，需从 `div.message.ai-message` 聊天气泡中提取全部内容（主回复 + 参考来源链接）并转发给用户
