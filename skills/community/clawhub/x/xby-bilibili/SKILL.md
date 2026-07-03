---
name: 哔哩哔哩API服务
description: 用于哔哩哔哩API的MCP服务器，支持视频搜索、用户内容获取等多种操作，适用于哔哩哔哩内容管理和数据分析场景。
version: 1.0.0
---

# 哔哩哔哩API服务

用于哔哩哔哩API的MCP服务器，支持视频搜索、用户内容获取等多种操作，适用于哔哩哔哩内容管理和数据分析场景。

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
| 
搜索哔哩哔哩用户信息。

Args:
    keyword: 用户名关键词
    page: 页码，默认为1

Returns:
    包含用户搜索结果的字典数据
 | `scripts.tools.search_user` |
| 
搜索并推荐相关视频，提供详细的推荐理由和总结

Args:
    keyword: 搜索关键词（如"AI"）
    count: 推荐视频数量，默认15条

Returns:
    包含推荐视频和总结的字典
 | `scripts.tools.search_and_recommend_videos` |
| 
通过用户名获取用户ID，支持精确搜索和详细信息返回

Args:
    username: 用户名
    return_details: 是否返回详细信息，默认False只返回用户ID

Returns:
    如果return_details=False: {"user_id": int} 或 {"error": str}
    如果return_details=True: {"users": list, "exact_match": bool} 或 {"error": str}
 | `scripts.tools.get_user_id_by_name` |
| 
获取视频的弹幕数据。支持视频链接或BV号输入。

Args:
    video_input: 视频链接或BV号
                支持格式：
                - BV号: BV1iv8CzVE2w
                - 完整链接: https://www.bilibili.com/video/BV1iv8CzVE2w/?spm_id_from=333.1387.homepage.video_card.click
                - 短链接: bilibili.com/video/BV1iv8CzVE2w
    page: 分P页码，从0开始，默认为0（第一个分P）

Returns:
    包含弹幕数据和视频信息的字典
 | `scripts.tools.get_video_danmaku` |
| 
获取指定用户的最新动态

Args:
    username: 用户名（如"技术爬爬虾"）
    count: 要获取的动态数量，默认10条

Returns:
    包含用户动态信息的字典
 | `scripts.tools.get_user_dynamics` |
| 
获取指定用户的最新投稿视频

Args:
    username: 用户名（如"技术爬爬虾"）
    count: 要获取的视频数量，默认10条

Returns:
    包含用户投稿视频信息的字典
 | `scripts.tools.get_user_videos` |
| 
获取指定用户的合集信息

Args:
    username: 用户名（如"技术爬爬虾"）

Returns:
    包含用户合集信息的字典
 | `scripts.tools.get_user_collections` |
| 
获取指定用户合集中的视频列表

Args:
    username: 用户名（如"技术爬爬虾"）
    collection_name: 合集名称，可选
    collection_id: 合集ID，可选
    count: 要获取的视频数量，默认10条

Returns:
    包含合集视频信息的字典
 | `scripts.tools.get_collection_videos` |
| 
在指定用户的所有合集中搜索包含关键词的视频

Args:
    username: 用户名（如"技术爬爬虾"）
    keyword: 搜索关键词（如"MCP"、"AI与大模型"等）
    count: 每个合集最多返回的视频数量，默认10条

Returns:
    包含搜索结果的字典
 | `scripts.tools.search_collection_by_keyword` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.search_user
工具描述：
搜索哔哩哔哩用户信息。

Args:
    keyword: 用户名关键词
    page: 页码，默认为1

Returns:
    包含用户搜索结果的字典数据

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|keyword|string|true| |null|
|page|integer|false|1.0|null|

---

## scripts.tools.search_and_recommend_videos
工具描述：
搜索并推荐相关视频，提供详细的推荐理由和总结

Args:
    keyword: 搜索关键词（如"AI"）
    count: 推荐视频数量，默认15条

Returns:
    包含推荐视频和总结的字典

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|keyword|string|true| |null|
|count|integer|false|15.0|null|

---

## scripts.tools.get_user_id_by_name
工具描述：
通过用户名获取用户ID，支持精确搜索和详细信息返回

Args:
    username: 用户名
    return_details: 是否返回详细信息，默认False只返回用户ID

Returns:
    如果return_details=False: {"user_id": int} 或 {"error": str}
    如果return_details=True: {"users": list, "exact_match": bool} 或 {"error": str}

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|username|string|true| |null|
|return_details|boolean|false|false|null|

---

## scripts.tools.get_video_danmaku
工具描述：
获取视频的弹幕数据。支持视频链接或BV号输入。

Args:
    video_input: 视频链接或BV号
                支持格式：
                - BV号: BV1iv8CzVE2w
                - 完整链接: https://www.bilibili.com/video/BV1iv8CzVE2w/?spm_id_from=333.1387.homepage.video_card.click
                - 短链接: bilibili.com/video/BV1iv8CzVE2w
    page: 分P页码，从0开始，默认为0（第一个分P）

Returns:
    包含弹幕数据和视频信息的字典

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|video_input|string|true| |null|
|page|integer|false|0.0|null|

---

## scripts.tools.get_user_dynamics
工具描述：
获取指定用户的最新动态

Args:
    username: 用户名（如"技术爬爬虾"）
    count: 要获取的动态数量，默认10条

Returns:
    包含用户动态信息的字典

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|username|string|true| |null|
|count|integer|false|10.0|null|

---

## scripts.tools.get_user_videos
工具描述：
获取指定用户的最新投稿视频

Args:
    username: 用户名（如"技术爬爬虾"）
    count: 要获取的视频数量，默认10条

Returns:
    包含用户投稿视频信息的字典

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|username|string|true| |null|
|count|integer|false|10.0|null|

---

## scripts.tools.get_user_collections
工具描述：
获取指定用户的合集信息

Args:
    username: 用户名（如"技术爬爬虾"）

Returns:
    包含用户合集信息的字典

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|username|string|true| |null|

---

## scripts.tools.get_collection_videos
工具描述：
获取指定用户合集中的视频列表

Args:
    username: 用户名（如"技术爬爬虾"）
    collection_name: 合集名称，可选
    collection_id: 合集ID，可选
    count: 要获取的视频数量，默认10条

Returns:
    包含合集视频信息的字典

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|username|string|true| |null|
|collection_name|string|false|""|null|
|collection_id|integer|false|0.0|null|
|count|integer|false|10.0|null|

---

## scripts.tools.search_collection_by_keyword
工具描述：
在指定用户的所有合集中搜索包含关键词的视频

Args:
    username: 用户名（如"技术爬爬虾"）
    keyword: 搜索关键词（如"MCP"、"AI与大模型"等）
    count: 每个合集最多返回的视频数量，默认10条

Returns:
    包含搜索结果的字典

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|username|string|true| |null|
|keyword|string|true| |null|
|count|integer|false|10.0|null|

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