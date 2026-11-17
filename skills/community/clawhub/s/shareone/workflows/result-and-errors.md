# 结果反馈与错误处理

发布、更新、上传或通用 API 请求完成后读取本文件。判断依据是**脚本的输出**：stdout 输出包含成功 JSON 或成功 token 即成功；stderr 输出 `ERROR:<code>` 即失败。

## 1. 发布成功

如果脚本 stdout 返回的 JSON 表示成功：

- 返回结果中已经包含完整的 `share_url` 字段，例如 `https://s.shareone.vip/s/<share_id>`。
- 必须直接使用返回的 `share_url` 展示给用户；不要展示备用链接。
- 如果返回中包含 `custom_slug_warning`，必须同时展示该提示；这表示内容已发布成功，但用户请求的自定义短链接没有生效。
- 如果返回中包含 `custom_slug_suggestions`，必须把其中的推荐短链接名称一起展示给用户。
- 不要自己拼接分享链接。
- 创建新分享链接时，在展示链接后简短提示保留规则：普通链接在 90 天内没有有效访问会被清理，持续有效访问则一直保持有效；Explore/知识库/`remote_url` 链接不受此限。对已有链接的 PUT 更新、设置修改、下载等非新建操作不要重复提示。

如果设置了密码，必须加粗显示密码：

> 发布成功！
> 链接：<返回的 share_url>
> 提取码：**<密码>**
> 保留规则：普通链接 90 天无有效访问会被清理，持续访问则保持有效。

## 2. 功能提示

在本次会话首次向用户展示生成的 `share_url` 时，必须主动但简短地提示所有未使用的高级功能。后续发布不再重复提示。

默认提示：

> 您也可以让我为这个分享链接设置自定义短链接名称、访问密码或水印。

按本次发布已经使用的能力删减提示内容：

- 如果用户已经指定自定义短链接，不再提示“自定义短链接名称”。
- 如果用户已经设置访问密码，不再提示“访问密码”。
- 如果用户已经设置水印，不再提示“水印”。
- 如果自定义短链接、访问密码、水印都已使用，不进行功能提示。

## 3. 自定义短链接冲突的两种行为

slug 冲突在两类发布中的表现**不同**，不要混淆：

- **文本页面（`/api/v1/pages`）**：slug 冲突会导致**发布失败**，返回 HTTP 400 且 `detail.code` 为 `CUSTOM_SLUG_TAKEN`。提示用户短链接名称已被占用；如果 `detail.suggested_slugs` 中包含推荐名称，必须一起展示。不要告诉用户“已发布成功”。
- **二进制文件（`/api/v1/files`）**：slug 冲突时**发布仍然成功**，返回中带 `custom_slug_warning`（和可能的 `custom_slug_suggestions`），只是自定义短链接没有生效。展示链接的同时必须展示该提示。

## 4. 非发布操作成功

对不一定返回 `share_url` 的操作，按脚本输出反馈结果：

- `update_share_settings.js`：stdout 为 JSON 且无 `ERROR:` 即设置更新成功。若 JSON 包含 `share_url`、`custom_slug_warning` 或 `custom_slug_suggestions`，按第 1 节展示；否则简短说明设置已更新。
- `comment_reply.js`：stdout 为服务端返回的 JSON。依据 `parent_status`、`parent_agent_stance` 和 `author_role` 判断实际结果；不从输入的 `--state` 推断成功。
- `shareone_api_request.js`：stdout 为接口返回体；用于查看评论时，摘要或列出评论即可，不要按发布成功话术处理。
- `download_share.js --save`：stdout 输出 `SAVED:<本地文件名>` 表示下载并保存成功；不要提示发布高级功能。

## 5. 常见错误

- 内容违规拦截，HTTP 400：提取 JSON 中的 `detail` 字段展示给用户，例如“发布失败，内容未通过安全审核。原因：<detail>”。
- 凭据错误 `AUTH_REQUIRED` / `INVALID_API_KEY`：检查当前账号的 Key，保留拥有原分享的身份。`FORBIDDEN` / `AGENT_OWNER_REQUIRED` 是权限问题，不要用新 guest Key 替换身份。密码和登录门禁分别按 `PASSWORD_REQUIRED` / `EMAIL_GATE_REQUIRED` 的 hint 处理。
- 找不到页面，HTTP 404：若 PUT 更新遇 404，说明原页面已被后台删除，请询问用户是否作为新页面重新 POST。
- 二进制文件被误发到 pages JSON 接口，HTTP 400 且提示检测到二进制内容：使用 `publish.js` 重新发布（它会自动分发到正确通道）；该错误只在绕过 `publish.js` 直接调用底层脚本时才可能出现。
- `ERROR:FILE_PREVIOUSLY_PUBLISHED`：该本地文件之前已发布过，错误提示中带有原 `share_id` 和链接。默认改用 `--share-id <id>` 更新原链接；只有用户明确要求为同一文件再创建一个新链接时，才追加 `--force-new` 重试。
- `ERROR:LOOKS_LIKE_SHARE_LINK`：把 ShareOne 链接当成本地文件传给了发布脚本。要修改已有链接设置用 `update_share_settings.js`，要下载用 `download_share.js`。
- `ERROR:UPDATE_VERIFY_FAILED`：不要按发布成功处理（即使 stdout 中已经输出了包含 `share_url` 的 JSON）。提示用户“ShareOne 接口接受了更新请求，但回读源内容与本地文件不一致，更新可能没有真正生效”，并保留本地文件，等待用户决定是否重试或作为新页面发布。
- `ERROR:ACTIVE_SHARE_TASK`：当前目录存在 `.shareone_active_task`（评论处理任务进行中），但发布命令没有带 `--share-id`。按错误提示中给出的 id 改用 `--share-id <id>` 执行 PUT 更新原链接；只有在确认用户确实要创建全新链接时，才删除该锚点文件或追加 `--force-new` 重试。
- `ERROR:UNKNOWN_ARGUMENT:<arg>` 或 `ERROR:MISSING_VALUE:<flag>`：命令参数写错或缺值。按脚本 Usage 修正命令，不要绕过脚本。
- `REMOTE_SOURCE_BOUND`（HTTP 409）：该页面已绑定远程源 URL，不能直接用 `html_content` 更新。错误返回中 `detail.remote_url` 包含源地址。告知用户去源头修改内容（如 GitHub 仓库文件或源 ShareOne 页面），所有引用该源的分享链接会自动同步。如果用户确实要改为本地内容，需要在 PUT 请求中同时传 `"remote_url": ""` 和 `"html_content": "..."` 来先解除绑定。
- 下载相关错误码（`PASSWORD_REQUIRED`、`PASSWORD_INVALID`、`DOWNLOAD_NOT_ALLOWED`、`SHARE_NOT_FOUND`）的处理见 `download-file.md`。

## 6. 错误与安全重试

脚本错误写入 stderr：稳定的 `ERROR:<CODE>`、`HINT`、`RETRYABLE`，以及完整的 `ERROR_JSON:{...}`；stdout 保留成功结果。退出码：输入 2、未找到 4、冲突 5、权限/门禁 6、凭据 7、限流 8、暂时故障 9，其他错误 1。`Retry-After` 保留在 `retry_after`。HTTP 响应增加 `error_code` / `hint` / `retryable`，原 `detail` 结构保持兼容。

页面创建、文件上传/确认、评论创建支持 `Idempotency-Key`。脚本可传 `--idempotency-key <key>`；同一账号、操作、键和请求内容返回原资源当前状态及 `idempotency_replayed: true`。不同内容重用同一键返回 `IDEMPOTENCY_CONFLICT`；原资源已删除返回 `OPERATION_RESOURCE_GONE`。幂等记录跨进程重启保留，只保存已提交资源引用。

发起操作前生成一次键并在重试时保留，例如 `crypto.randomUUID()`；事件处理可用 `event.id + 操作名`。重放的内容必须一致。不要为新的用户意图复用旧键；未支持幂等键的 POST 不能因为网络错误就盲目重发。二进制脚本带键时使用单次 multipart 创建；直接上传工作流重试确认时必须保留原 `share_id` 和内容。
