# 管理 ShareOne 链接的协作者

当用户要求添加或移除协作者、查看协作者列表或检查谁有权限访问某个 ShareOne 链接时读取本文件。执行前必须已经完成 `environment-and-credentials.md`。

本 workflow 只管理协作者权限，不修改内容、水印、密码等元数据。

## 1. 判断是否适用

适用示例：

- "给这个 ShareOne 链接添加协作者：https://shareone.app/s/xxx"
- "Add a collaborator to this share"
- "列出这个分享链接的协作者"
- "移除这个链接的某个协作者"
- "谁有权限访问这个分享链接？"
- "让别人一起编辑这个页面"
- "分享编辑权限给同事"
- "对方怎么拿 API Key？"

协作者按 ShareOne **用户名**标识（不是 API Key）——这是安全设计，避免在协作管理里传递密钥。如果用户要求添加或移除协作者但没有提供协作者的用户名，先询问协作者的用户名。协作者可在自己的设置页或通过 `GET /api/v1/me` 查到自己的用户名；对方不知道怎么获取时，按第 6 节引导。

## 2. 不要做的事

- 不要下载源文件。
- 不要修改页面内容或元数据（水印、密码等）。
- 不要使用 `upload_page.js` 或 `update_share_settings.js`。

## 3. 管理命令

### 列出协作者

```bash
node scripts/manage_collaborators.js "<SHARE_LINK_OR_ID>" --action list
```

### 添加协作者

```bash
node scripts/manage_collaborators.js "<SHARE_LINK_OR_ID>" --action add --usernames "alice,bob"
```

### 移除协作者

```bash
node scripts/manage_collaborators.js "<SHARE_LINK_OR_ID>" --action remove --usernames "alice,bob"
```

规则：

- Sudowork 环境不要传 `--api-key`。
- 普通 AI Agent 环境可传 `--api-key`，也可以依赖 `SHAREONE_API_KEY` 或本地凭证。
- `--usernames` 参数为要添加或移除的协作者的 ShareOne 用户名，多个用逗号分隔。
- 脚本会自动从完整 URL、`/s/<ref>` 路径、裸 `share_id` 或 slug 中解析目标。

## 4. 结果解读

- `--action list`：返回当前协作者列表的 JSON。
- `--action add`：返回添加后的结果 JSON，确认哪些协作者已成功添加。
- `--action remove`：返回移除后的结果 JSON，确认哪些协作者已成功移除。

## 5. 下一步

执行完成后读取 `result-and-errors.md`，按返回 JSON 展示结果或错误。

## 6. 协作者如何提供 username

添加协作者只需要对方的 **username**（公开标识），不需要 API Key（私密凭证）。

### 对方有 AI Agent

让对方的 agent 调用 `GET /api/v1/me`（需要凭据）查看自己的 username，然后把 username 告诉 owner。

### 对方没有 AI Agent

Owner 的 agent 可以代替对方创建 guest 账号。**必须使用 `--no-save`**，否则会覆盖 owner 自己的 API Key：

```bash
node scripts/create_guest_key.js --no-save
```

将返回的 key 发给对方保存。guest 用户的 username 是自动生成的（如 `guest_e7ead86a`），owner 需要知道这个 username 才能添加协作者。对方的 agent 用该 key 调 `GET /api/v1/me` 获取 username 后告知 owner。

### 协作者拿到权限后能做什么

- **下载**：用自己的 API Key 调用 `GET /api/v1/shares/{share_id}/download` 下载源内容
- **编辑更新**：修改内容后用 `PUT /api/v1/pages/{share_id}` 上传更新（只能改内容，不能改密码、水印等设置）
- **处理评论**：可以解决或关闭评论

### 建议对方绑定邮箱

添加协作者成功后，如果对方使用的是 guest key，建议提醒对方绑定邮箱（按 `workflows/bind-account.md` 流程），以便后续在网站上管理文件。
