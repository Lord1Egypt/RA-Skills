# CLI Contract

## 版本

```bash
python3 scripts/lexiang_upload.py --version
```

```json
{"name":"upload-markdown-to-lexiang","version":"1.3.1","cli_api":"1"}
```

调用方只依赖 `cli_api`、命令行参数和 JSON 字段，不 import 内部模块。

## 鉴权

唯一方式是 <https://lexiangla.com/ai/claw> 提供的个人凭证：

- `mcp_token`：`lxmcp_` 前缀 MCP API Token。
- `company_from`：租户标识。
- 请求头：`Authorization: Bearer <mcp_token>`。

```bash
python3 scripts/lexiang_upload.py auth login
python3 scripts/lexiang_upload.py auth login --file "<页面导出的凭证.json>" [--profile NAME | --credential-file PATH]
python3 scripts/lexiang_upload.py auth status [--check] [--profile NAME | --credential-file PATH]
python3 scripts/lexiang_upload.py auth logout [--profile NAME | --credential-file PATH]
```

default profile 的凭证路径保持为 `~/.config/lexiang-upload/credentials.json`；
显式 `--profile default` 也使用该旧路径。命名 profile 使用
`~/.config/lexiang-upload/profiles/<profile>.json`，名称仅允许
`[A-Za-z0-9._-]`。所有 auth 子命令和 upload 均支持 `--profile NAME` 与
`--credential-file PATH`。

选择优先级为：显式 `--credential-file` > 显式 `--profile` >
`LEXIANG_UPLOAD_CREDENTIALS` > `LEXIANG_UPLOAD_PROFILE` > default。
`auth login --file` 表示从导出文件读取凭证内容；`--credential-file` 才选择保存目标。

## 上传参数

- `upload <md>`：Markdown 文件。
- `--work-dir DIR --md FILE`：兼容工作包形式。
- `--parent-id ID`：新建 page 的父目录。
- `--entry-id ID`：覆盖已有 page。
- `--name NAME`：页面名称；默认依次取 meta title、首个 H1、文件名。
- `--name-suffix TEXT`：显式标题后缀，默认空。
- `--pin`：新建后置顶，默认关闭。
- `--source-url URL` / `--source-title TITLE`：显式插入原文链接，优先级最高。
- `--meta-file FILE`：读取调用方元信息，但不会隐式使用其中的 parent/source。
- `--parent-from-meta`：显式启用 meta `parent_id`。
- `--source-from-meta`：显式启用 meta source。URL 依次取显式 `--source-url`、
  `meta.source_url`；仍无 URL 且有 `meta.entry_id` 时生成乐享页面 URL。标题依次取
  显式 `--source-title`、`meta.source_title`、`meta.title`。
- `--formula-mode unicode|image|native|hybrid`：默认 `unicode`。
- `--dry-run`：仅预检，不读取凭证、不写线上。
- `--json`：成功时输出稳定 JSON。
- `--profile NAME`：选择 default 或命名凭证 profile。
- `--credential-file PATH`：直接选择凭证文件，优先级高于 profile。

## 可移植富文档标注

上传器在本地 preflight 识别以下连续 blockquote，并直接规划、创建乐享原生 callout：

```markdown
> [!stat] **73%**
> English statistic.
> 中文统计。

> [!definition] **Specific stiffness**
> English definition.
> 中文定义。

> [!note] **文章亮点**
> - **亮点一：**组织管理类比
> - **亮点二：**Evals 是新的 OKRs
```

`stat` 使用 📊，`definition` 使用 📖，`note` 使用 💡。普通 Markdown blockquote 保持原转换行为。
调用方不得在上传后通过 MCP 二次替换这些标注。

## 成功输出

```json
{
  "ok": true,
  "action": "created",
  "entry_id": "...",
  "page_url": "...",
  "title": "...",
  "local_images": 8,
  "remote_images": 8,
  "local_callouts": 2,
  "remote_callouts": 2,
  "verified": true,
  "credential_profile": "default",
  "credential_file": "~/.config/lexiang-upload/credentials.json",
  "company_from": "...",
  "cli_api": "1",
  "version": "1.3.1"
}
```

`--dry-run` JSON 包含 `local_callouts`，不包含尚未产生的 `remote_callouts`。线上
执行成功后会同时返回二者，并对 callout 数量和内容做验证。dry-run 不读取凭证，
但会安全返回 `credential_profile` / `credential_file`；任何 JSON 都不会输出 token。

## 退出码

- `0`：成功。
- `2`：本地预检失败。
- `3`：个人凭证缺失、失效或被撤销。
- `4`：网络或乐享写入失败。
- `5`：线上内容对账失败。
