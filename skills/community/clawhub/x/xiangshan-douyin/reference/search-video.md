# 关键词搜索抖音视频

根据关键词搜索抖音视频，返回匹配结果及其视频元数据和互动指标。

## 使用说明

用户需要提供以下参数（通过 $ARGUMENTS 传入或交互式询问）：

- `keyword`（必填）: 搜索关键词
- `page`（可选，默认 1）: 页码
- `searchId`（可选）: 搜索ID，翻页时使用上一次返回的 search_id
- `sortType`（可选，默认 `_0`）: 排序类型
  - `_0` = 综合排序
  - `_1` = 最多点赞
  - `_2` = 最新发布
- `publishTime`（可选，默认 `_0`）: 发布时间筛选
  - `_0` = 不限
  - `_1` = 一天内
  - `_7` = 一周内
  - `_182` = 半年内
- `duration`（可选，默认 `_0`）: 视频时长筛选
  - `_0` = 不限
  - `_10` = 0-10秒
  - `_30` = 10-30秒
  - `_60` = 30-60秒
  - `_300` = 1-5分钟
  - `_1800` = 5-30分钟
  - `_1801` = >30分钟

## 执行步骤

1. 从 $ARGUMENTS 中解析参数。如果参数不完整，向用户询问缺失的必填参数。
2. 读取 API Key：优先从环境变量 `XS_API_KEY` 获取，如果未设置则向用户询问。
3. 使用 curl 调用接口（注意：这是 GET 请求）：

```bash
curl -s --location 'https://api.xsdata.top/api/v1/douyin/search-video?keyword=<keyword>&page=<page>&searchId=<searchId>&sortType=<sortType>&publishTime=<publishTime>&duration=<duration>' \
--header 'x-api-key: <api_key>' \
--header 'Content-Type: application/json'
```

4. 解析返回的 JSON。数据嵌套在 `data.business_data[].data.aweme_info` 中。提取关键字段以表格形式呈现：

   对每个搜索结果视频：
   - `aweme_id`（视频ID）
   - `desc`（视频描述/标题）
   - `create_time`（发布时间，转换为可读日期）
   - `author.nickname`（作者昵称）
   - `author.unique_id`（作者抖音号）
   - `statistics.digg_count`（点赞数）
   - `statistics.comment_count`（评论数）
   - `statistics.share_count`（分享数）
   - `statistics.play_count`（播放数）
   - `video.duration`（视频时长，转换为 分:秒）
   - `video.cover`（封面图URL）

5. 如果 `has_more` 为 1，提示用户可以翻页查看更多结果，并展示翻页所需的 `search_id`。
6. 如果 `success` 为 false，展示错误信息给用户。

## 注意事项

- 该接口消耗 API 积分，请提醒用户
- 搜索结果中的 `aweme_id` 可直接用于「获取视频详情」和「获取视频评论」接口
- 搜索结果中的 `author.sec_uid` 可用于「获取用户详细资料」接口
- 结果数据量较大时只展示前几条并询问用户是否需要查看更多
