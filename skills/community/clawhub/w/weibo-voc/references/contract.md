# 输出信封

stdout 只有一份 JSON。日志在 stderr。

```json
{
  "status": "success",
  "error_code": "OK",
  "message": "搜索任务完成",
  "timestamp": "2026-11-25 21:40:00",
  "request": {},
  "metadata": {
    "skill_version": "1.0.0",
    "runtime_version": "v22.0.0",
    "execution_time": 1200,
    "total": 50
  },
  "results": [],
  "cost": 0.1
}
```

- `status`：`success` / `empty` / `error`。
- `empty` 的 `error_code` 是 `NO_MATCH`，退出码 0。`results` 省略。
- `cost` 没有时整字段省略。热搜按次；搜索约每 10 条一页；评论约每 20 条一页。
- `metadata.total` 只在热搜成功时出现，等于榜单条数。搜索和评论看 `results.length`。
- `request` 只含本次命令参数（`command`、`category`、`keyword`、`search_type`、`url`、`sort`、`limit`）。不含任务 uuid。

创建接口返回的 `id` 只在进程内部使用：随后的查询只传这个 `id`。对外超时后，用同一组业务参数再执行一次即可续等。

## results 里看什么

热搜每条常见字段：`rank`、`title`、`hot`、`label`、`query`、`flag`。向用户摘排名、标题、热度。

搜索每条常见字段：`text`、`url`、`created_at`、`reposts_count`、`comments_count`、`attitudes_count`、`user`。用户搜索看 `user`（`name`、`followers_count`、`description`）。话题看 `topic`，超话看 `chaohua`。有视频时看 `video`。

评论每条常见字段：`text`、`created_at`、`like_counts`、`user.screen_name`。楼中楼在 `comments`。

向用户摘这些字段。不要粘贴整份 JSON。
