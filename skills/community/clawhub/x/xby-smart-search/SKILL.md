---
name: 智能搜索工具集
description: Smart Search MCP 是一个专注于技术领域的智能搜索工具集，提供14个增强型搜索工具，覆盖国际和国内主流技术平台，具备智能URL生成、输入验证、高级搜索技巧等功能，适用于开发者快速查找技术文档、API参考、开源项目等。
version: 1.0.0
---

# 智能搜索工具集

Smart Search MCP 是一个专注于技术领域的智能搜索工具集，提供14个增强型搜索工具，覆盖国际和国内主流技术平台，具备智能URL生成、输入验证、高级搜索技巧等功能，适用于开发者快速查找技术文档、API参考、开源项目等。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| 🔍 网络搜索 - 通用网络搜索（Google/Bing/百度/搜狗）

【重要】此工具会返回搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_web` |
| 🐙 GitHub搜索 - 搜索GitHub仓库、代码、问题和用户

【重要】此工具会返回GitHub搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_github` |
| 💬 StackOverflow搜索 - 搜索技术问题和解决方案

【重要】此工具会返回StackOverflow搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_stackoverflow` |
| 📦 NPM包搜索 - 搜索NPM包和相关文档

【重要】此工具会返回NPM搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_npm` |
| 📚 技术文档搜索 - 搜索常见框架和工具的官方文档（React、Vue、Node.js等）

【重要】此工具会返回文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_docs` |
| 🔗 API参考搜索 - 快速查找API文档和使用示例

【重要】此工具会返回API文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_api_reference` |
| 📱 微信开发者文档搜索 - 搜索微信小程序、公众号、开放平台文档

【重要】此工具会返回微信文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_wechat_docs` |
| 📝 CSDN搜索 - 搜索CSDN技术博客和问答

【重要】此工具会返回CSDN搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_csdn` |
| 💎 掘金搜索 - 搜索掘金技术社区文章

【重要】此工具会返回掘金搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_juejin` |
| 🔧 SegmentFault搜索 - 搜索思否技术问答和文章

【重要】此工具会返回SegmentFault搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_segmentfault` |
| 📚 博客园搜索 - 搜索博客园技术博客

【重要】此工具会返回博客园搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_cnblogs` |
| 🌐 开源中国搜索 - 搜索开源中国技术资讯和项目

【重要】此工具会返回开源中国搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_oschina` |
| ☁️ 阿里云文档搜索 - 搜索阿里云产品文档和API

【重要】此工具会返回阿里云文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_aliyun_docs` |
| ☁️ 腾讯云文档搜索 - 搜索腾讯云产品文档和API

【重要】此工具会返回腾讯云文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。 | `scripts.tools.ai_search_tencent_docs` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.ai_search_web
工具描述：🔍 网络搜索 - 通用网络搜索（Google/Bing/百度/搜狗）

【重要】此工具会返回搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |搜索关键词|
|engine|string|false|"baidu"|搜索引擎，默认baidu|
|count|number|false|10.0|期望的结果数量，默认10|

---

## scripts.tools.ai_search_github
工具描述：🐙 GitHub搜索 - 搜索GitHub仓库、代码、问题和用户

【重要】此工具会返回GitHub搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |搜索关键词|
|type|string|false|"repositories"|搜索类型，默认repositories|
|language|string|false| |编程语言筛选（可选）|
|sort|string|false|"stars"|排序方式，默认stars|

---

## scripts.tools.ai_search_stackoverflow
工具描述：💬 StackOverflow搜索 - 搜索技术问题和解决方案

【重要】此工具会返回StackOverflow搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |搜索关键词或问题描述|
|tags|string|false| |标签筛选（如：javascript,react）|
|sort|string|false|"relevance"|排序方式，默认relevance|

---

## scripts.tools.ai_search_npm
工具描述：📦 NPM包搜索 - 搜索NPM包和相关文档

【重要】此工具会返回NPM搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |包名或关键词|
|size|number|false|10.0|返回结果数量，默认10|

---

## scripts.tools.ai_search_docs
工具描述：📚 技术文档搜索 - 搜索常见框架和工具的官方文档（React、Vue、Node.js等）

【重要】此工具会返回文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |搜索关键词|
|framework|string|false|"general"|指定框架，默认general|

---

## scripts.tools.ai_search_api_reference
工具描述：🔗 API参考搜索 - 快速查找API文档和使用示例

【重要】此工具会返回API文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|api_name|string|true| |API名称或方法名|
|platform|string|true| |平台或库名称（如：express、axios、lodash）|

---

## scripts.tools.ai_search_wechat_docs
工具描述：📱 微信开发者文档搜索 - 搜索微信小程序、公众号、开放平台文档

【重要】此工具会返回微信文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |搜索关键词|
|platform|string|false|"all"|平台类型|

---

## scripts.tools.ai_search_csdn
工具描述：📝 CSDN搜索 - 搜索CSDN技术博客和问答

【重要】此工具会返回CSDN搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |搜索关键词|
|type|string|false|"all"|搜索类型|

---

## scripts.tools.ai_search_juejin
工具描述：💎 掘金搜索 - 搜索掘金技术社区文章

【重要】此工具会返回掘金搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |搜索关键词|
|sort|string|false|"hot"|排序方式|

---

## scripts.tools.ai_search_segmentfault
工具描述：🔧 SegmentFault搜索 - 搜索思否技术问答和文章

【重要】此工具会返回SegmentFault搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |搜索关键词|
|tags|string|false| |标签筛选（可选）|

---

## scripts.tools.ai_search_cnblogs
工具描述：📚 博客园搜索 - 搜索博客园技术博客

【重要】此工具会返回博客园搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |搜索关键词|

---

## scripts.tools.ai_search_oschina
工具描述：🌐 开源中国搜索 - 搜索开源中国技术资讯和项目

【重要】此工具会返回开源中国搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |搜索关键词|
|type|string|false|"all"|搜索类型|

---

## scripts.tools.ai_search_aliyun_docs
工具描述：☁️ 阿里云文档搜索 - 搜索阿里云产品文档和API

【重要】此工具会返回阿里云文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |搜索关键词|
|product|string|false| |产品名称（如：ecs、oss、rds等）|

---

## scripts.tools.ai_search_tencent_docs
工具描述：☁️ 腾讯云文档搜索 - 搜索腾讯云产品文档和API

【重要】此工具会返回腾讯云文档搜索URL，Claude Code应该使用WebFetch工具访问该URL以获取真实搜索结果。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |搜索关键词|
|product|string|false| |产品名称（如：cvm、cos、cdn等）|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据