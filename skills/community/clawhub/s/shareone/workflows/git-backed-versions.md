# 用 Git 管理 ShareOne 内容版本

当用户要为 ShareOne 内容选择 Git 源、跟随分支、固定版本、查看历史、回退版本，或修改 Git 源上的内容时读取本文件。GitHub / GitLab 保存内容历史、diff、分支和评审；ShareOne 通过 `remote_url` 提供展示与评论。ShareOne 的缓存会被刷新覆盖，不提供独立的历史版本、diff 或回滚 API。

## 1. 当前可用范围

| 源 | 当前处理方式 |
| --- | --- |
| 公开 GitHub `.html` / `.md` / `.txt` 文件 | 可直接绑定 HTTPS `github.com/.../blob/...` 或 `raw.githubusercontent.com` 文件 URL；blob 自动转 raw |
| GitHub 私有仓库 | 当前没有仓库凭据接入，不能假定 ShareOne 能读取；保留仓库原有访问范围，不把 token 拼进 URL |
| GitLab / 企业 GitLab | 当前域名白名单不含 GitLab；接入域名、服务端网络和仓库认证后才可绑定 remote URL。已有仓库也可按 §3.1 手动发布选定版本的本地文件 |
| 本地文件上传 | 按原发布流程保存当前内容；不会自动建立 Git 历史或绑定仓库 |
| ShareOne 内链 pointer | 多个分享同步同一份源内容，可各设密码/水印；不保存源的历史版本 |

这些 remote-url 步骤适用于文本页面；PDF/PPT/Word 继续使用 `publish-binary-file.md`。只查看历史时读取源仓库即可；需要创建、绑定、切换或刷新分享时，先完成 `environment-and-credentials.md` 的凭据检查。更新 remote URL 和强制刷新要求分享 owner 权限；仓库读写权限由 Git 平台单独管理。

完整原生 HTML 的远程源上限为 16 MiB。遇到审核拒绝或 `CONTENT_REVIEW_REQUIRED`，保留拒绝记录，按用户授权走 [content-review.md](content-review.md)；不另选版本或改成其他上传方式绕过拒绝。正式批准仅适用于审核记录中的文件哈希、源 URL、页面和访问设置。

## 2. 选择跟随分支或固定 commit

以下 `org/repo`、文件路径、`<FULL_COMMIT_SHA>` 和 `<REF>` 都要替换成实际值。命令从 skill 安装目录执行；创建新分享还需遵守 `publish-text-page.md` 的发布规则。

**持续更新的页面：绑定分支文件 URL。** 源仓库合并新内容后，同一 ShareOne 链接可拉取更新。

```bash
node scripts/upload_page.js --remote-url "https://github.com/org/repo/blob/main/docs/report.html"
```

**需要固定文件版本：绑定完整 commit SHA。** 同一 commit 的文件内容不会随分支推进而改变；标签可能被移动，固定版本时优先使用完整 SHA。

```bash
node scripts/upload_page.js --remote-url "https://github.com/org/repo/blob/<FULL_COMMIT_SHA>/docs/report.html"
```

只有用户要求协同评论时才加 `--allow-comments true`。已有分享要绑定 Git 源或切换版本时，加 `--share-id <REF>`；`<REF>` 是原分享的稳定 ID 或 slug：

```bash
node scripts/upload_page.js --share-id <REF> --remote-url "https://github.com/org/repo/blob/<FULL_COMMIT_SHA>/docs/report.html"
```

这会更新原分享并保留其评论；省略 `--share-id` 会创建另一个分享。需要保持原链接时，不改 slug、不使用 `--force-new`。既有 `.shareone_active_task` 中的目标仍然有效。

## 3. 修改源内容并同步

1. 确认源仓库、文件和当前 ref。已有分享可用 `node scripts/download_share.js "<REF>" --save` 查看 owner 下载返回的 `INFO:REMOTE_SOURCE`；下载得到的是 ShareOne 当前缓存，源 URL 仅在有权限的下载中返回。
2. 在源仓库修改并验证，通过该仓库现有的提交、评审和发布流程，使修改进入分享绑定的分支。沿用已有授权；ShareOne 的 API Key 不提供 Git push 或合并权限。
3. 若分享固定到 commit，旧 URL 会继续读取旧 commit。要展示新版本，先按 §2 用原 `--share-id` 换成选定的新 commit URL；不要默默切回分支。
4. 对绑定分支的原分享立即刷新：

```bash
node scripts/refresh_share.js "<REF>"
node scripts/download_share.js "<REF>" --save
```

检查刷新 JSON 中的 `remote_last_error`，并核对下载内容包含预期修改。只有 HTTP 成功或出现 `SHARE_REFRESHED` 不能证明已更新：抓取失败时可能继续保留旧缓存。自然刷新只在打开渲染页时触发，受 60 秒下限、无 ETag 时 10 分钟 TTL 限制；下载本身不会触发刷新。

远程源页面不能通过上传本地副本覆盖正文，会返回 `REMOTE_SOURCE_BOUND`。先修改源头再刷新；不为绕过错误自动解绑。若没有仓库写权限，交付修改建议或按已有权限创建 PR，说明尚待合并/同步的步骤。

### 3.1 从 Git 仓库手动发布本地文件

GitLab 或私有仓库尚不能直连时，若用户采用手动同步，可用已有仓库访问权限取出选定 commit 的文本文件，再走本地发布流程。文件历史仍保存在 Git 仓库；ShareOne 不会自动跟随后续提交。

```bash
# 更新已有、未绑定 remote URL 的分享；首次创建才省略 --share-id
node scripts/publish.js "<LOCAL_REPO_FILE>" --share-id <REF>
```

确认发布文件与选定 commit 一致，避免把未提交的本地修改标成该 commit。按 `publish-text-page.md` 验收原分享，并记录源仓库/commit 链接。以后换版或回退时，取出所选版本再更新同一分享；不为采用此路径自动解绑已有 remote 源。

## 4. 查看历史与回退

- **查看历史 / diff**：到已确认的源仓库查看文件历史、提交或比较页面。不要编造 ShareOne 版本查询 API，也不要把缓存时间、ETag 当成 commit。
- **让原分享展示旧文件版本**：从仓库历史确认目标完整 SHA，按 §2 更新原分享的 `remote_url`，保留原 ID 和评论。这会固定到该 commit。
- **继续跟随分支并撤销一次修改**：按源仓库流程用 revert 提交撤销，再刷新原分享；不需要重写 Git 历史。

结果中说明分享链接、源文件 URL，以及当前是跟随分支还是固定 commit。提交链接可供追溯；这不是 ShareOne 自动记录的版本关联。

## 5. 评论针对的是哪一版

当前评论按分享 ID 保存，尚未自动关联 Git commit。切换源版本后，已有评论保留，但锚点可能不再匹配；不能从评论时间或当前分支 HEAD 推断评论创建时的版本。

处理评论仍走 `comments-process.md` 的认领和回复步骤；Git 源的修改在仓库完成，原分享同步并验收后才回复 `resolved-agree`。可在回复中附本次修复的 commit/PR 链接；这标识修复来源，不代表已知道原评论对应的 commit。等待权限、评审或同步时说明剩余步骤，使用 `open-need-input` 保持待处理。
