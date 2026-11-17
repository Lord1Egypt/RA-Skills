---
name: upload-markdown-to-lexiang
version: "1.3.1"
author: ajaxhe
license: MIT
category: productivity
description: >-
  Upload a Markdown document with local images and formulas to an editable
  Tencent Lexiang page. Performs local preflight, deterministic mixed
  text/image upload, and remote verification. Use when publishing Markdown to
  Lexiang or when another skill needs the shared lexiang-upload CLI.
  将 Markdown 图文文档可靠上传为乐享在线文档，供归档、PDF 翻译和笔记同步 Skill 复用。
tags: markdown, lexiang, upload, knowledge-base, images
disable-model-invocation: false
---

# Upload Markdown to Lexiang

这是 Markdown → 乐享在线文档的唯一公共上传层。抓取、翻译、目录策略、增量同步等业务逻辑应留在上层 Skill。
可移植 Markdown 中的目标专有标注解析与乐享块渲染属于本 Skill，不由调用方上传后修补。

## 硬性规则

1. 上传代码只维护在本 Skill；禁止复制到调用方。
2. 只使用从 <https://lexiangla.com/ai/claw> 获取的个人凭证。
3. 禁止读取 Agent MCP 配置、连接器 OAuth token 或扫描本地代理。
4. 创建或修改页面前完成全部本地预检，写入后必须线上对账。
5. stdout 只输出 JSON/页面 URL，诊断和进度输出到 stderr。

## 定位本 Skill

调用方不得写死某个 Agent 的安装目录。按以下顺序定位：

1. 环境变量 `LEXIANG_UPLOADER_HOME`。
2. 当前上层 Skill 所在 `skills` 根目录的同级 Skill：
   `<skills-root>/upload-markdown-to-lexiang`。
3. 当前 Agent 暴露的已安装 Skill 列表。
4. 当前平台的 Skill 管理器默认安装目录。

用户 ajaxhe 的本地开发默认目录是
`~/.workbuddy/skills/upload-markdown-to-lexiang`，这不是跨用户公共契约。

定位后调用：

```bash
python3 "<skill-root>/scripts/lexiang_upload.py" --version
```

上层 Skill 必须要求 `cli_api == "1"`，不得 import 内部 Python 模块。

## 首次配置个人凭证

页面提供的凭证是 `lxmcp_` 前缀 MCP API Token 和 `company_from`。本 Skill
直接使用 `Authorization: Bearer <lxmcp_token>`，不做 OAuth token 交换。

```bash
python3 "<skill-root>/scripts/lexiang_upload.py" auth login
python3 "<skill-root>/scripts/lexiang_upload.py" auth status --check
```

凭证默认保存在 `~/.config/lexiang-upload/credentials.json`，权限为 `0600`，
不会写进 Skill 或 Git 仓库。

多账号可使用命名 profile，保存到
`~/.config/lexiang-upload/profiles/<profile>.json`：

```bash
python3 "<skill-root>/scripts/lexiang_upload.py" auth login \
  --profile obsidian-sync
python3 "<skill-root>/scripts/lexiang_upload.py" auth status \
  --profile obsidian-sync --check
python3 "<skill-root>/scripts/lexiang_upload.py" upload article.md \
  --profile obsidian-sync --parent-id "<PARENT_ID>" --json
```

也可用 `--credential-file PATH` 指定凭证保存/读取位置。`auth login --file PATH`
表示从导出文件读取凭证内容，不是保存目标。选择优先级为：
`--credential-file`、`--profile`、`LEXIANG_UPLOAD_CREDENTIALS`、
`LEXIANG_UPLOAD_PROFILE`、default；default 始终对应原有 `credentials.json`。

## 上传

创建新页面：

```bash
python3 "<skill-root>/scripts/lexiang_upload.py" upload article.md \
  --parent-id "<PARENT_ID>" --name "标题" --json
```

覆盖已有页面：

```bash
python3 "<skill-root>/scripts/lexiang_upload.py" upload article.md \
  --entry-id "<ENTRY_ID>" --json
```

只做预检：

```bash
python3 "<skill-root>/scripts/lexiang_upload.py" upload article.md \
  --parent-id "<PARENT_ID>" --dry-run --json
```

## 调用方职责

- 调用方只负责确定 `parent_id`、`entry_id` 和归档策略（标题、置顶、来源等）。
- 本 Skill 负责 Markdown 解析、本地图片、公式转换、目标专有标注渲染、页面写入和线上对账。
- 本地图片路径支持 `%20`、未转义空格及 `<images/file name.png>` 形式；所有识别到的
  本地图片都必须进入预检与线上数量对账。
- `> [!stat]`、`> [!definition]` 与 `> [!note]` 连续 blockquote 由本 Skill分别渲染为
  📊/📖/💡 乐享 callout；`note` 可承载文章亮点列表。调用方禁止二次 MCP 修补。
  普通 blockquote 不受影响。
- 非 Markdown 独立附件、视频和音频不属于本 Skill。

完整参数、JSON 输出和退出码见 [references/cli-contract.md](references/cli-contract.md)。

## 修改与验证

发现公共上传问题时，只修改本仓库并运行：

```bash
python3 -m unittest discover -s tests -v
```

兼容改动升级次版本；破坏 CLI 契约时升级主版本和 `cli_api`。
