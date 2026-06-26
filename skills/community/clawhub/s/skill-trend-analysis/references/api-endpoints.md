# Skill Trend Analysis API 端点速查

Base URL: `http://skills.easytoken.cc/api`

## 核心只读接口

- `GET /skills`
  - 参数：`fields`、`format=csv`
- `GET /skills/top`
  - 参数：`limit`、`order=downloads|stars|updated_at|created_at`
- `GET /skills/{skill_id}`
- `GET /skills/search`
  - 参数：`q`、`tag`、`owner`、`min_downloads`、`min_stars`、`limit`
- `GET /skills/growth`
  - 参数：
    - `start_date`、`end_date`（ISO 日期）
    - 或 `days`（默认 7）
    - `metric=downloads|stars`
    - `rank_limit`（默认 1000）
    - `limit`（默认 100）
    - `min_growth`
- `GET /skills/time-range`
  - 参数：`start_date`、`end_date`、`date_field`、`order`、`limit`
- `GET /stats`
- `GET /stats/time-range`
- `GET /tags`
- `GET /authors`
- `GET /export`

## 调试建议

- 做趋势分析时，优先看 `/skills/growth`、`/skills/top`、`/skills/time-range`、`/stats/time-range`
- 如果用户要求“最近几天”但未给绝对日期，可优先使用 `days`
- 如果用户要求可复现分析，回答中写明 `metric`、时间窗口、`rank_limit`、`limit`
- 看 HTTP 码：
  ```bash
  curl -o /dev/null -s -w "%{http_code}\n" "http://skills.easytoken.cc/api/stats"
  ```
- 触发限流后重试：等待 3 秒。
