# 查看 ShareOne 评论

当用户只是要求查看、拉取、总结评论时读取本文件。不要修改源文件，不要认领评论，不要关闭评论。

开放分享允许匿名读取。完整列表、摘要、增量查询和截图均遵守密码、登录与评论开关；owner/协作者可用已有 API Key 跳过访问者门禁。`comment_list.js` 会使用已有凭据，也允许开放分享的匿名读取；不需要为查看评论新建身份。

## 1. 获取 ref

用户提供的目标可以是完整链接、`/s/<ref>` 或 `/md/<ref>` 路径、裸 `share_id` 或自定义短链 slug。取路径最后一段作为 `<REF>` 即可，接口同时接受 `share_id` 和 slug。

## 2. 查看评论

优先用 `comment_list.js`——它输出干净的 UTF-8 JSON（`{ share, status, count, comments:[{ id, status, author_role, quote, content, created_at, updated_at, screenshot_url, agent_stance, viewer_can_manage, resolution_note, reply_count, replies:[...] }] }`），省去手工拼接 endpoint 和解析原始响应，也规避控制台非 ASCII 乱码：

```bash
node scripts/comment_list.js <REF>                 # 默认 --status all
node scripts/comment_list.js <REF> --status open   # 只看未处理
node scripts/comment_list.js <REF> --json compact  # 单行 JSON，便于管道解析
```

`--status` 可选值：

- `all`（默认）
- `open`
- `in_progress`
- `resolved`
- `dismissed`
- `unresolved`，等价于 `open + in_progress`

评论已关闭时返回 `ERROR:COMMENTS_DISABLED`（403），表示该分享不提供评论读取，不能据此判断 API Key 无效。告知用户评论已关闭；只有用户明确要求开启时，才按 [update-share-settings.md](update-share-settings.md) 修改开关。

受限分享需要授权。密码门禁返回 `PASSWORD_REQUIRED`，登录门禁返回 `EMAIL_GATE_REQUIRED`；按 hint 完成访问授权，保持当前账号 Key。

截图路径以 `/comment-screenshots/` 开头时，相对正在访问的 ShareOne origin 解析，发送同一 origin 的已验证 Cookie 或 owner/协作者凭据。

## 3. 评论理解规则

- 只展示评论内容，绝对不要自作主张开始修改源文件。
- 等用户明确要求“处理这些评论”、“根据评论改一下页面”等，再进入 `comments-process.md`。
- 评论数据中可能包含 `replies`。必须将父评论及其所有回复作为一个 thread 整体阅读，综合理解最终共识。
- 不要把每条回复当成独立修改指令。
- 所有回复继承父评论的锚点，也就是 `highlighter_data` 和 `quote`。
- 父评论的 `quote` / `highlighter_data` 是原始捕获，有 `anchor_binding` 时使用其中的目标作为当前绑定。`comment_list.js` 会保留完整的 `anchor_binding`、绑定版本及 `viewer_can_reattach`，不会把当前绑定伪装为原始选区。回复属于同一线程，按父线程的当前绑定阅读。
- 原始 SDK 对象评论可以没有文字范围。不能从对象标题、评论时间或 Git 分支猜出原始选中文字。用户明确要求重新选择目标时，读取 [comment-reattachment.md](comment-reattachment.md)；普通查看不触发重绑。

## 4. 轻量摘要

如果只想看“现在还有没有未处理的事”，用摘要接口：

```bash
node scripts/shareone_api_request.js "/api/v1/shares/<REF>/comments/summary" --public
# -> { total, open, in_progress, resolved, dismissed, last_activity_at }
```

返回 `open + in_progress == 0` 时没有待处理线程；需要阅读历史内容时仍可拉取列表。

## 5. 增量维护评论缓存

需要持续更新一个评论视图时，可以复用通用请求脚本：

```bash
node scripts/shareone_api_request.js "/api/v1/shares/<REF>/comments/changes" --public
node scripts/shareone_api_request.js "/api/v1/shares/<REF>/comments/changes?cursor=<URL_ENCODED_CURSOR>&limit=100" --public
```

首次省略 `cursor`，用 `reset=true` 的 `comments` 替换缓存；包括上线前已有的评论。后续按顶层 ID 替换返回的完整线程（含回复），删除 `deleted_ids`，应用成功后保存 `next_cursor`。`has_more=true` 时立即继续；`limit` 是事件数，默认 100、最大 200。线程反映当前状态，同一批可幂等重放。400 表示游标无效，应重新获取快照。游标只对原分享有效。

此接口每次检查页面密码/登录要求。`--public` 适用于没有访问门槛的分享；有 owner/协作者凭据时省略 `--public`。浏览器访问者使用页面授权 Cookie；本脚本不会代填页面密码。`comment_list.js` 保留截图、AI 立场、更新时间、权限字段和嵌套回复，只省略较大的 `highlighter_data`。

该接口只读，不注册消费者或确认事件。需要可靠接收通知并唤醒 Agent 时，使用 `agent-notifications.md` 的持久消费者流程。
