# 处理 ShareOne 评论

当用户明确要求“处理这些评论”、“根据评论改一下页面”、“修改这个 ShareOne 链接的内容”时读取本文件。只查看评论时不要读取本文件。

ShareOne 页面评论包含状态机字段 `status`：`open` / `in_progress` / `resolved` / `dismissed`，以及作者字段 `author_role`：`visitor` / `owner` / `agent`。

处理评论需要 owner 的 API Key（认领状态、发 agent 回复都要求 owner 鉴权），执行前必须已经完成 `environment-and-credentials.md`。

## 1. 获取 ref 与评论

用户提供的目标可以是完整链接、`/s/<ref>` 或 `/md/<ref>` 路径、裸 `share_id` 或自定义短链 slug。取路径最后一段作为 `<REF>` 即可，接口同时接受 `share_id` 和 slug。

本 workflow 只适用于可编辑的文本/HTML/Markdown 页面评论处理。若目标链接路径明确是 `/pdf/`、`/ppt/`、`/word/`，或下载后的 `INFO:CONTENT_TYPE`/文件扩展名显示为 PDF/PPT/Word 等二进制文档，不要为处理评论解析、转换或修改二进制正文；停止内容修改流程，并告知用户当前 skill 只支持处理页面源码评论，二进制文档只能查看/总结评论或更新元数据设置。

任务锚点：步骤 2 的下载命令（`--task-anchor`）会自动把 `<REF>` 写入当前目录的 `.shareone_active_task` 文件，把目标 share 固定到磁盘上（防止长时间编辑文件后上下文丢失，误把更新发成新链接）。后续所有步骤中的 `<REF>` 都以该文件内容为准；任何时候不确定目标 share 是哪个，读取该文件，**不要凭记忆，更不要新建链接**。

先获取未处理评论：

```bash
node scripts/shareone_api_request.js "/api/v1/shares/<REF>/comments?status=unresolved"
```

评论数据中可能包含 `replies`。必须将父评论及其所有回复作为一个 thread 整体阅读，综合理解最终共识。回复不需要单独走流程，只对父评论操作状态。

“当前视图隐藏”表示页面确认目标存在；“等待页面定位目标”表示尚无当前证据；“目标在当前版本中已不存在”只用于页面完整模型明确报告缺失的 ID；“文字无法定位，内容可能已变化”仍是旧文字匹配失败。区域评论同时保留各部分数量。不要从显示名猜测稳定 ID，不自动把旧文字评论改绑到对象。评论仍可阅读和回复；定位状态不能替代用户对反馈的判断，也不能自动 dismiss 或关闭评论。动态 HTML 的接入与性能验收见 `publish-text-page.md` 的“动态页面与文字评论”。

## 2. 标准闭环流程

对每条要处理的父评论，严格按以下顺序执行。

### 步骤 1：认领

必须在动手之前做：

```bash
node scripts/shareone_api_request.js "/api/v1/shares/<REF>/comments/<COMMENT_ID>/status" \
  --method PUT \
  --data '{"status": "in_progress"}'
```

访问者会立刻在页面侧栏看到“处理中”徽标和顶部“AI 正在处理 N 条评论...”横幅。跳过这一步会让用户感受不到 AI 在干活。

### 步骤 2：取源（自动写锚点）

```bash
node scripts/download_share.js "<REF>" --task-anchor
```

`--task-anchor` 会自动完成三件事：写入 `.shareone_active_task` 锚点（stderr 输出 `ANCHOR_WRITTEN:`）、按服务端文件名的扩展名把源内容保存为 `shareone_<REF>_source.<ext>`（stdout 输出 `SAVED:<本地文件名>`）、在 stderr 输出 `INFO:FILENAME:`（原始文件名，步骤 4 要用）和 `INFO:CONTENT_TYPE:`。文件名携带目标 share，即使对话上下文丢失也能恢复 `<REF>`。已配置 owner API Key 时脚本自动走 owner 下载接口，不受密码和下载开关限制。

**根据下载信息选择修改位置：**

- 未绑定远程源：编辑 `SAVED:` 给出的本地文件，按步骤 4A 更新原分享。
- 出现 `INFO:REMOTE_SOURCE` / `HINT:EDIT_AT_SOURCE`：下载的是远程源的缓存副本。先读 [git-backed-versions.md](git-backed-versions.md)，在对应 Git 仓库修改，按步骤 4B 同步原分享。若源是另一个 ShareOne 分享，则修改那个源 share 后刷新当前分享；保留当前 `.shareone_active_task` 作为回复目标，不用它替代源 share 的 ID。

### 步骤 3：精准应用修改

定位前检查父线程的 `anchor_binding`：有绑定时使用其 `quote` / `highlighter_data`，否则使用父评论原始字段。完整捕获可通过通用脚本读取评论列表；`comment_list.js` 保留当前绑定，但省略原始较大的 `highlighter_data`。原始字段用于历史证据，不能覆盖当前绑定。找不到当前目标时保持反馈状态并澄清；用户明确要求重新绑定才读 [comment-reattachment.md](comment-reattachment.md)。

- 综合理解整个 thread（父评论 + 所有 replies）的最终意图，必要时先和用户确认。
- 绝对不要用全局 `replace()` 或正则批量替换，会误伤其他同名文案。
- 基于 DOM 结构精确定位：利用 `highlighter_data.startMeta.parentTagName`、`parentIndex`、`textOffset`，结合 `quote`（被选中原文）定位准确节点。
- 理解结构性意图：评论可能是“把这部分挪到底部 / 删掉这个区块 / 加个图标”，先定位再做结构变更。
- 如果无法定位原文，先保留评论与原文，用 `comment_reply.js --state open-need-input` 说明缺少的信息并等待澄清。定位失败不能证明内容不存在，也不能成为 dismiss 的依据。

### 步骤 4：更新并验收原分享（保留目标 ID）

#### 4A. 未绑定远程源：PUT 上传正文

脚本选择说明：更新**内容**只能用 `publish.js --share-id`（带 `--share-id` 时执行的是 PUT 内容更新，不是创建）；`update_share_settings.js` 只能改密码/水印/短链/评论开关等元数据，**无法替换页面内容**，本步骤不要使用它。

直接执行以下命令更新原链接。`<REF>` 与步骤 1、2、5 是同一个值，即 `.shareone_active_task` 文件的内容：

```bash
node scripts/publish.js "<步骤 2 SAVED: 给出的本地文件>" --filename "<INFO:FILENAME 给出的原文件名>" --share-id <REF>
```

硬规则：

- 评论处理流程中**禁止**不带 `--share-id` 执行发布命令——那会 POST 创建一个全新链接，原链接和上面已认领的评论都不会得到任何更新。
- 不要跳读 `publish-text-page.md` 的“判断创建还是更新”一节，评论场景永远是更新，没有“首次创建”分支。
- 如果此刻想不起 `share_id`，读取 `.shareone_active_task` 文件或源文件名中的 `shareone_<REF>_` 前缀，绝不新建。
- 如果脚本输出 `ERROR:ACTIVE_SHARE_TASK`，说明漏传了 `--share-id`，按错误提示补上后重试。

评论闭环中的重新发布属于对已有链接的更新，**不需要**向用户展示发布前安全提示或等待确认（规则见入口 `SKILL.md`）。

#### 4B. 绑定远程源：修改源头后刷新

Git 源按仓库现有流程提交、评审和合并到绑定分支，然后执行 `node scripts/refresh_share.js "<REF>"`。固定 commit 的分享，先按 `git-backed-versions.md` 用原 `--share-id` 换成已选定的新 commit URL。ShareOne 内链则更新源 share 后刷新当前分享。

核对 `remote_last_error` 并下载确认预期修改已进入原分享，再执行步骤 5。不要对远程源页面用 `publish.js` 上传缓存副本；遇到 `REMOTE_SOURCE_BOUND` 不自动解绑。没有源仓库权限、PR 尚待合并或同步失败时，说明剩余步骤，用 `open-need-input` 保持待处理。可附修复 commit/PR 链接，但当前评论没有自动绑定创建时的 commit。

### 步骤 5：回复评论并**强制表态**（一条命令，`--state` 必填）

每次回复评论都**必须**用 `comment_reply.js` 并声明一个 `--state`——这是硬性要求（缺省即报错），目的是杜绝“只回复不收敛 / 有分歧却没 signal 出来 / 不确定却没保持 open”这三种失败模式：

```bash
# 同意并已按建议修改 → 评论收敛为 resolved
node scripts/comment_reply.js "<REF>" <COMMENT_ID> --content "已按你的建议把标题改成 ...，并调整了 ..." --state resolved-agree
```

`--state` 三选一（无默认）：

| state | 含义 | 对父评论的作用 |
|---|---|---|
| `resolved-agree` | 充分理解且同意，已处理 | 置 `resolved` |
| `open-disagree` | 不同意（在 `--content` 里写清理由） | **保持 `open`**，标记“AI 有异议”，把是否关闭交回给提出者 |
| `open-need-input` | 需要人类进一步澄清/输入 | 保持 `open` |

后端会从父评论继承 `quote`/`highlighter_data`，以 `author_role=agent` 保存回复，并据 `--state` 原子地设置父评论状态与 AI 立场。脚本 stdout 返回回复 JSON，核对 `id`、`parent_status` 和 `parent_agent_stance`；不要手工拼接含 `highlighter_data` 的 JSON。

**关键原则：AI 永不单方面关闭一条分歧。** 不同意时用 `open-disagree`（保持 open、让提出者决定），**绝不**用 dismiss 把别人的评论关掉——关闭/重开一条评论的权力属于提出评论的人（以及页面 owner）。

- 输出 `ERROR:STATE_REQUIRED` / `ERROR:INVALID_STATE`：必须补上合法的 `--state`。
- 输出 `ERROR:IS_REPLY:<parent_id>`：传入的是回复 ID，改用父评论 ID 重试。
- 输出 `ERROR:COMMENTS_DISABLED`（403）：评论已关闭，停止评论处理并告知用户。只有用户明确要求开启时，才按 [update-share-settings.md](update-share-settings.md) 修改开关。

如果误发了一条回复，可以删除（仅作者本人、且父评论仍为 `open` 时可删，会级联删除其回复）：

```bash
node scripts/shareone_api_request.js "/api/v1/shares/<SHARE_ID>/comments/<COMMENT_ID>" --method DELETE
```

## 3. 无关或垃圾评论

**注意区分“不同意”与“无关”**：对你有异议但属于合理讨论的评论，用步骤 5 的 `--state open-disagree`（保持 open），**不要** dismiss。`dismiss` 只用于**owner 确认的无关或垃圾评论**的评论（例如指向了另一份分享、垃圾评论）——这是 owner 的否决动作：

```bash
node scripts/shareone_api_request.js "/api/v1/shares/<REF>/comments/<COMMENT_ID>/status" --method PUT --data '{"status":"dismissed","note":"owner 确认这是垃圾评论"}'
```

确认返回 JSON 的 `status` 为 `dismissed`。无法定位、权限不足、源 PR 待合并或刷新失败时，用 `open-need-input` 并说明原因。

## 4. 收尾：删除任务锚点

所有目标评论都已 `resolved` 或 `dismissed`、且重新发布完成后，删除任务锚点文件：

```bash
rm -f .shareone_active_task
```

不删除的话，之后正常的新页面发布会被发布脚本拦截（`ERROR:ACTIVE_SHARE_TASK`）。

## 5. 兼容旧接口

旧接口仍然可用，但新代码不要使用：

```http
PUT /api/v1/shares/<REF>/comments/<COMMENT_ID>/resolve
{ "resolved": true/false }
```

它等价于把 `status` 切到 `resolved` 或 `open`，但不会附带 `note`，访问者拿不到 AI 的解释。新代码一律使用 `/status` 接口。

## 6. 关键准则速查

| 准则 | 为什么 |
| --- | --- |
| 动手前先 `in_progress` | 让访问者看到“AI 在干活” |
| 改完一定要 `POST` 一条 `author_role=agent` 的回复 | 闭环的“答复”部分，没有它就只是状态变化、不是对话 |
| `note` 要写人话 | “已把按钮改成主色” 比 “Applied.” 有用 |
| 信息或权限不足时 `open-need-input` | 保留待办并说明需要的人类输入 |
| 只对父评论改状态，回复不单独操作 | 状态语义属于 thread 整体 |
| `unresolved` = `open + in_progress` | 拉单子默认用 `?status=unresolved` |
