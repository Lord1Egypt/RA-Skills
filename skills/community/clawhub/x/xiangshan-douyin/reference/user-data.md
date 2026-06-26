# 获取抖音用户详细资料

获取抖音用户的详细资料信息。

## 使用说明

用户需要提供以下参数（通过 $ARGUMENTS 传入或交互式询问）：

- `sec_user_id` 或 `share_text`（二选一必填）
  - `sec_user_id`: 抖音用户的 sec_user_id
  - `share_text`: 用户主页分享文本/链接

## 执行步骤

1. 从 $ARGUMENTS 中解析参数。如果参数不完整，向用户询问缺失的必填参数。
2. 读取 API Key：优先从环境变量 `XS_API_KEY` 获取，如果未设置则向用户询问。
3. 使用 curl 调用接口：

```bash
curl -s --location 'https://api.xsdata.top/api/v1/goa/douyin/fetch-user-data' \
--header 'x-api-key: <api_key>' \
--header 'Content-Type: application/json' \
--data '{
  "sec_user_id": "<sec_user_id>",
  "share_text": "<share_text>"
}'
```

4. 解析返回的 JSON，提取关键字段并以清晰的形式呈现给用户：
   - `nickname`（昵称）
   - `uid`（用户ID）
   - `short_id`（短ID）
   - `signature`（个人简介）
   - `avatar_larger`（头像URL）
   - 粉丝数 `follower_count`
   - 关注数 `following_count`
   - 获赞数 `total_favorited`
   - 作品数 `aweme_count`
   - `is_verified`（是否认证）
   - `verification_type`（认证类型）
   - `ip_location`（IP 属地）
   - 其他有意义的用户画像字段

5. 如果 `success` 为 false，展示错误信息给用户。

## 注意事项

- 该接口消耗 API 积分，请提醒用户
- `sec_user_id` 和 `share_text` 至少填写一个
- 可以接受用户直接粘贴抖音个人主页的分享链接作为 `share_text`
