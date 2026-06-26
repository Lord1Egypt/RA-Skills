# 关键词搜索抖音用户

通过关键词搜索抖音用户，返回包含昵称、头像、粉丝数及其他元数据的用户资料。

## 使用说明

用户需要提供以下参数（通过 $ARGUMENTS 传入或交互式询问）：

- `keyword`（必填）: 搜索关键词（用户昵称/抖音号）
- `page`（可选，默认 1）: 页码
- `userType`（可选）: 用户类型筛选

## 执行步骤

1. 从 $ARGUMENTS 中解析参数。如果参数不完整，向用户询问缺失的必填参数。
2. 读取 API Key：优先从环境变量 `XS_API_KEY` 获取，如果未设置则向用户询问。
3. 使用 curl 调用接口（注意：这是 GET 请求）：

```bash
curl -s --location 'https://api.xsdata.top/api/v1/douyin/search-user?keyword=<keyword>&page=<page>&userType=<userType>' \
--header 'x-api-key: <api_key>' \
--header 'Content-Type: application/json'
```

4. 解析返回的 JSON。注意：返回数据嵌套结构为 `data.business_data[].data.raw_data`（raw_data 是 JSON 字符串，需要二次解析）。提取关键字段并以表格形式呈现：

   对每个搜索结果用户：
   - `nickname`（昵称）
   - `uid`（用户ID）
   - `unique_id`（抖音号）
   - `sec_uid`（sec_user_id，可用于其他接口查询）
   - `follower_count`（粉丝数，需格式化如 566.9万）
   - `avatar_larger`（头像URL）
   - `signature`（个人简介）
   - `verification_type`（认证类型）
   - `custom_verify`（自定义认证信息）

5. 如果 `has_more` 为 1，提示用户可以翻页查看更多结果。
6. 如果 `success` 为 false，展示错误信息给用户。

## 注意事项

- 该接口消耗 API 积分，请提醒用户
- raw_data 是 JSON 字符串，需要 JSON.parse 二次解析
- 粉丝数需要格式化显示（如 5669200 → 566.9万）
- 搜索结果中的 `sec_uid` 可直接用于「获取用户详细资料」和「获取用户主页视频列表」接口
