# 查看 ShareOne 评论

当用户只是要求查看、拉取、总结评论时读取本文件。不要修改源文件，不要认领评论，不要关闭评论。

查看评论走公开接口，**不需要 API Key**，命令统一加 `--public`；只有进入处理评论流程（`comments-process.md`）时才需要凭据。

## 1. 获取 ref

用户提供的目标可以是完整链接、`/s/<ref>` 或 `/md/<ref>` 路径、裸 `share_id` 或自定义短链 slug。取路径最后一段作为 `<REF>` 即可，接口同时接受 `share_id` 和 slug。

## 2. 查看未处理评论

调用：

```bash
node scripts/shareone_api_request.js "/api/v1/shares/<REF>/comments?status=unresolved" --public
```

`status` 可选值：

- `all`
- `open`
- `in_progress`
- `resolved`
- `dismissed`
- `unresolved`，等价于 `open + in_progress`

## 3. 评论理解规则

- 只展示评论内容，绝对不要自作主张开始修改源文件。
- 等用户明确要求“处理这些评论”、“根据评论改一下页面”等，再进入 `comments-process.md`。
- 评论数据中可能包含 `replies`。必须将父评论及其所有回复作为一个 thread 整体阅读，综合理解最终共识。
- 不要把每条回复当成独立修改指令。
- 所有回复继承父评论的锚点，也就是 `highlighter_data` 和 `quote`。

## 4. 轻量摘要

如果只想看“现在还有没有未处理的事”，用摘要接口：

```bash
node scripts/shareone_api_request.js "/api/v1/shares/<REF>/comments/summary" --public
# -> { total, open, in_progress, resolved, dismissed, last_activity_at }
```

返回 `open == 0` 时无需拉全量评论。
