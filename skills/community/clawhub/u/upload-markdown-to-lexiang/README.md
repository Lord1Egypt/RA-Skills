# Upload Markdown to Lexiang

Markdown 图文文档到腾讯乐享在线文档的公共上传 Skill。

## 特性

- 标准 Markdown 与相对本地图片
- `> [!stat]` / `> [!definition]` 可移植标注转乐享原生 callout
- 创建或覆盖 page
- Unicode、图片或实验性原生公式模式
- 上传前完整预检
- 上传后标题、正文锚点、图片和公式对账
- 稳定 JSON 输出和退出码
- 仅使用乐享个人凭证，支持多 profile

版本 `1.3.1` 保持 `cli_api="1"`。使用 `--source-from-meta` 时，来源 URL 优先取
`meta.source_url`，标题优先取 `meta.source_title` 再取 `meta.title`；显式
`--source-url` / `--source-title` 始终优先。没有 `source_url` 但存在 `entry_id`
时，仍回退为对应乐享页面 URL。

## 安装位置

不要依赖固定 Agent 目录。建议安装到调用方 Skill 所在的同一个 skills 根目录：

```text
<skills-root>/
├── upload-markdown-to-lexiang/
├── fetch-archive-to-lexiang/
└── sync-obsidian-to-lexiang/
```

作者本机默认开发目录是
`~/.workbuddy/skills/upload-markdown-to-lexiang`，但这不是公共路径契约。

## 凭证

访问 <https://lexiangla.com/ai/claw> 获取个人凭证：

凭证包含 `lxmcp_` 前缀的 MCP API Token 和 `company_from`。登录命令支持直接
粘贴页面复制的凭证 JSON、URL 或安装指令。

```bash
bin/lexiang-upload auth login
bin/lexiang-upload auth status --check
```

无参数时继续使用旧路径 `~/.config/lexiang-upload/credentials.json`。命名 profile
保存在 `~/.config/lexiang-upload/profiles/<profile>.json`：

```bash
bin/lexiang-upload auth login --profile obsidian-sync
bin/lexiang-upload auth status --profile obsidian-sync --check
bin/lexiang-upload upload article.md --profile obsidian-sync \
  --parent-id <PARENT_ID> --json
```

`--credential-file PATH` 可直接选择凭证文件，优先级高于 `--profile`。
`auth login --file PATH` 只负责读取导出的凭证内容，不决定保存位置。完整优先级：
`--credential-file` > `--profile` > `LEXIANG_UPLOAD_CREDENTIALS` >
`LEXIANG_UPLOAD_PROFILE` > default。

## 上传

```bash
bin/lexiang-upload upload article.md \
  --parent-id <PARENT_ID> \
  --name "标题" \
  --json
```

更新已有页面：

```bash
bin/lexiang-upload upload article.md --entry-id <ENTRY_ID> --json
```

调用方只负责 `parent_id`、`entry_id` 和归档策略。目标专有 Markdown 标注的解析、
乐享块渲染和线上对账均由 uploader 完成，调用方不应再用 MCP 二次修补。

## 测试

```bash
python3 -m unittest discover -s tests -v
```
