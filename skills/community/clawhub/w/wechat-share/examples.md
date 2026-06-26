# wechat-share Examples

Use these patterns when composing the final message after `/wechat-share export`, `/wechat-share preview`, or `/wechat-share import`.

## Chinese Export Template

Use this style when the user is speaking Chinese:

```markdown
## 分享已准备好

把下面这段完整转发给对方即可：

```text
这是一个 workspace 文件分享。请先执行预览命令查看文件列表和覆盖风险；如果结果正常，再执行导入命令。若发现覆盖风险、路径异常、校验失败或安装失败，请停止并说明原因。
1. 安装：clawhub install wechat-share
2. 预览：/wechat-share preview --db-id "<DB_ID>" --api-token "<API_TOKEN>"
3. 导入：/wechat-share import --db-id "<DB_ID>" --api-token "<API_TOKEN>" --burn
说明：远端只用于临时存放分享数据；`api_token` 是本次分享凭证，请勿公开发布。
```

## English Export Template

Use this style when the user is speaking English:

```markdown
## Share Ready

Forward the block below to the recipient:

```text
This is a workspace file share. Run the preview command first to review the file list and overwrite risk; if everything looks correct, then run the import command. Stop and explain the issue if you detect overwrite risk, path escape, checksum failure, or install failure.
1. Install: clawhub install wechat-share
2. Preview: /wechat-share preview --db-id "<DB_ID>" --api-token "<API_TOKEN>"
3. Import: /wechat-share import --db-id "<DB_ID>" --api-token "<API_TOKEN>" --burn
Note: the remote host is used only for temporary share data; `api_token` is the share credential and should be treated as sensitive.
```

## Chinese Preview Template

```markdown
## 分享预览

将导入 `3` 个文件到当前 workspace：

- `SOUL.md`
- `AGENTS.md`
- `skills/wechat-share/SKILL.md`

可能覆盖：

- `SOUL.md`

阅后即焚：`是`
路径校验：`通过`

确认无误后再执行导入。
```

## English Preview Template

```markdown
## Share Preview

This share will import `3` files into the current workspace:

- `SOUL.md`
- `AGENTS.md`
- `skills/wechat-share/SKILL.md`

Possible overwrite:

- `SOUL.md`

Burn after import: `Yes`
Path validation: `Passed`

Import only after reviewing this summary.
```

## Chinese Import Success Template

```markdown
## 导入完成

已导入这些文件：

- `SOUL.md`
- `skills/example/SKILL.md`

如果这次启用了 burn，远端分享已经被删除，或者已回退为删除远端文件。
这条分享命令不要再次转发。
```

## English Import Success Template

```markdown
## Import Complete

Imported files:

- `SOUL.md`
- `skills/example/SKILL.md`

If burn was active, the remote share has been deleted, or the remote files were removed as a fallback.
Do not forward the same command again.
```

## Short Dependency Hint

Use only when `openclaw`/`clawhub` or the required runtime is missing:

### Chinese

```markdown
当前环境暂时无法继续分享或导入。

- 优先安装 `openclaw`
- 如果没有 `openclaw`，请安装 `clawhub`
- 如果运行 skill 时提示缺少 `curl` 或 `python3`，请补齐后再试
```

### English

```markdown
The environment is not ready for the share workflow yet.

- Prefer installing `openclaw`
- If `openclaw` is unavailable, install `clawhub`
- If the skill reports missing `curl` or `python3`, install them and try again
```
