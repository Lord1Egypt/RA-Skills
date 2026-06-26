# tweet-thread 兼容说明

`tweet-thread` 已升级为更通用的 `x-like-posts` 路线。

请改读：

[references/x-like-posts.md](x-like-posts.md)

兼容规则：

- 新正式脚本是 `render_x_like_posts.py`
- `render_tweet_thread.py` 仅保留兼容包装
- 旧参数 `--tweet` / `--tweets-file` 仍可继续使用
- 新推荐参数是 `--post` / `--posts-file`
