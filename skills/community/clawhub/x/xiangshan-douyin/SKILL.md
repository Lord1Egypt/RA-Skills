---
name: xiangshan-douyin
description: 向善数据抖音 API 工具集。搜索抖音用户/视频，获取用户资料、视频详情、评论、播放量统计数据。TRIGGER when user wants to search Douyin users/videos, fetch user profile, video details, video comments, or video play statistics.
---

# 向善数据 - 抖音 API 工具集

根据用户的需求，智能选择并调用对应的抖音数据 API 接口。

## API 基础信息

- **域名**: `https://api.xsdata.top`
- **认证方式**: 请求 Header 中携带 `x-api-key`
- **API Key 获取**: 优先从环境变量 `XS_API_KEY` 读取，如果未设置则向用户询问

## 可用接口

根据用户意图，选择最合适的接口执行。如果用户意图不明确，询问用户需要查询什么数据。

### 1. 获取用户主页视频列表

- **触发场景**: 用户想查看某抖音博主发布的视频列表
- **接口**: `POST /api/v1/goa/douyin/fetch-user-video-list`
- **必填参数**: `sec_user_id` 或 `share_text`（二选一）
- **可选参数**: `count`（默认10）、`max_cursor`（翻页游标）、`filter_type`
- **详细参考**: 参考 `reference/user-video-list.md`

### 2. 获取用户详细资料

- **触发场景**: 用户想查看某抖音博主的详细资料（粉丝数、简介等）
- **接口**: `POST /api/v1/goa/douyin/fetch-user-data`
- **必填参数**: `sec_user_id` 或 `share_text`（二选一）
- **详细参考**: 参考 `reference/user-data.md`

### 3. 获取视频详情

- **触发场景**: 用户想查看某条抖音视频的详细信息（播放量、点赞数等）
- **接口**: `POST /api/v1/goa/douyin/fetch-video-detail`
- **必填参数**: `aweme_id` 或 `share_text`（二选一）
- **详细参考**: 参考 `reference/video-detail.md`

### 4. 获取视频一级评论

- **触发场景**: 用户想查看某条抖音视频的评论列表
- **接口**: `POST /api/v1/goa/douyin/fetch-video-comment`
- **必填参数**: `aweme_id` 或 `share_text`（二选一）
- **可选参数**: `count`（默认10）、`cursor`（翻页游标）
- **详细参考**: 参考 `reference/video-comment.md`

### 5. 关键词搜索用户

- **触发场景**: 用户想通过关键词搜索抖音用户（昵称/抖音号）
- **接口**: `GET /api/v1/douyin/search-user`
- **必填参数**: `keyword`（搜索关键词）
- **可选参数**: `page`（页码）、`userType`（用户类型）
- **注意**: 返回数据中 `raw_data` 是 JSON 字符串，需要二次解析
- **详细参考**: 参考 `reference/search-user.md`

### 6. 关键词搜索视频

- **触发场景**: 用户想通过关键词搜索抖音视频
- **接口**: `GET /api/v1/douyin/search-video`
- **必填参数**: `keyword`（搜索关键词）
- **可选参数**: `page`、`searchId`（翻页）、`sortType`（排序：`_0`综合/`_1`最多点赞/`_2`最新）、`publishTime`（时间筛选：`_0`不限/`_1`一天内/`_7`一周内）、`duration`（时长筛选：`_0`不限/`_10`0-10s/`_30`10-30s/`_60`30-60s/`_300`1-5min）
- **详细参考**: 参考 `reference/search-video.md`

### 7. 获取视频统计数据（含播放数）

- **触发场景**: 用户想获取视频的播放量（其他接口不返回播放数）
- **接口**: `POST /api/v1/goa/douyin/fetch-video-statistics`
- **必填参数**: `aweme_id` 或 `share_text`（二选一）
- **返回数据**: `digg_count`（点赞）、`download_count`（下载）、`play_count`（播放）、`share_count`（分享）
- **详细参考**: 参考 `reference/video-statistics.md`

## 请求模板

POST 接口：

```bash
curl -s --location 'https://api.xsdata.top<endpoint>' \
--header 'x-api-key: <api_key>' \
--header 'Content-Type: application/json' \
--data '<json_body>'
```

GET 接口：

```bash
curl -s --location 'https://api.xsdata.top<endpoint>?<query_params>' \
--header 'x-api-key: <api_key>' \
--header 'Content-Type: application/json'
```

## 用户输入解析规则

- 如果用户粘贴了抖音分享链接（如 `https://v.douyin.com/xxx`），将其作为 `share_text` 参数
- 如果用户提供了 `aweme_id`（纯数字ID），用于视频相关接口
- 如果用户提供了 `sec_user_id`（以 `MS4wLjAB` 开头的长字符串），用于用户相关接口
- 如果用户只说了博主昵称但没有提供 ID，先用搜索用户接口搜索，找到 `sec_uid` 后再调用用户相关接口
- 如果用户想搜索视频，使用搜索视频接口，支持排序和时间/时长筛选
- 如果用户特别关心播放量数据，使用视频统计接口（其他接口不返回播放数）

## 执行步骤

1. 分析用户输入，判断意图和数据类型
2. 选择合适的 API 接口
3. 提取或询问必要参数
4. 读取 API Key（环境变量 `XS_API_KEY` 或询问用户）
5. 发起请求并解析结果
6. 以清晰易读的方式展示关键数据
7. 提示用户是否需要进一步操作（翻页、查看详情、查看评论等）

## 注意事项

- 所有接口都消耗 API 积分，请在调用前提醒用户
- 返回数据可能较大，只展示用户关心的核心字段
- 鼓励用户将 API Key 设置为环境变量 `XS_API_KEY` 以便后续使用
