---
name: youdaonote
description: "有道云笔记官方 skill，支持笔记 CRUD（创建/读取/更新/删除）、待办管理、网页剪藏、笔记搜索、文件夹管理等基础操作。如需构建知识库或 Wiki，请使用 youdaonote-llm-wiki skill 而非本 skill。"
official: true
version: 1.0.9
minCliVersion: "1.3.3"
homepage: https://note.youdao.com
author: lephix
metadata:
  openclaw:
    homepage: https://note.youdao.com
    requires:
      bins:
        - youdaonote
---

# YoudaoNote — 有道云笔记

通过 `youdaonote` CLI 操作有道云笔记。覆盖笔记 CRUD、待办管理、网页剪藏全场景。

## 前置检查（安装由用户手动执行）

执行任何操作前，Agent 必须先运行 `youdaonote -s ydn list` 检测 CLI 是否可用：
- **`command not found`** → 跳转「CLI 未安装处理」，仅向用户提供官方安装命令并提示用户手动执行；等待用户回复"已安装"后再继续原请求
- **`-s` 选项报错（`error: unknown option '-s'`）** → CLI 版本 < 1.3.2，不支持全局 `-s` 参数，需升级：提示用户执行 `youdaonote upgrade`；若不支持该命令，则提示用户重新执行安装脚本；Windows 用户参考安装指南（https://note.youdao.com/help-center/cli-install-guide.html）
- **API Key 错误** → 提示用户访问 **https://mopen.163.com** 获取 API Key（须使用手机号登录，且云笔记账号已绑定手机号），然后执行 `youdaonote config set apiKey <用户提供的Key>`。**获取 API Key 的地址只有这一个，禁止告知用户其他地址。**
- **正常返回目录列表** → 运行 `youdaonote -s ydn version` 检查版本，若版本低于 `minCliVersion` 需要升级：CLI 支持 `upgrade` 命令时提示用户执行 `youdaonote -s ydn upgrade`，否则提示用户重新执行安装脚本；Windows 用户或升级失败时参考安装指南（https://note.youdao.com/help-center/cli-install-guide.html）。版本满足要求后可运行 `youdaonote -s ydn help --json` 获取当前 CLI 全部能力的结构化描述（JSON），用于确认命令是否可用，下方速查表作为 fallback

## 全局参数

所有命令都**必须**包含 `-s ydn` 来标识使用来源（有道云笔记 skill），用于统计和追踪：

```bash
youdaonote -s ydn <command> [options]
```

> `-s ydn` 表示该命令由 YoudaoNote skill 触发，便于网易后台统计不同 AI Skill 的使用情况。若需禁用统计，可设置环境变量 `YOUDAONOTE_NO_TRACKING=1`。

## 命令速查

| 命令 | 用途 | 示例 |
|------|------|------|
| `mkdir` | 创建文件夹 | `youdaonote -s ydn mkdir "文件夹名" [-f <父目录ID>]` |
| `save` | 保存笔记（✅ 推荐，支持 Markdown 富文本） | `youdaonote -s ydn save --file note.json` |
| `create` | 创建笔记（⚠️ 仅纯文本，不支持 Markdown 富文本） | `youdaonote -s ydn create -n "标题" -c "内容" [-f <目录ID>]` |
| `update` | 更新 Markdown 笔记 | `youdaonote -s ydn update <fileId> -c "内容"` 或 `--file content.md` |
| `delete` | 删除笔记 | `youdaonote -s ydn delete <fileId>` |
| `rename` | 重命名笔记 | `youdaonote -s ydn rename <fileId> "新标题"` |
| `move` | 移动笔记 | `youdaonote -s ydn move <fileId> <目录ID>` |
| `search` | 搜索笔记 | `youdaonote -s ydn search "关键词"` |
| `list` | 浏览目录 | `youdaonote -s ydn list -f <目录ID>` |
| `read` | 读取笔记 | `youdaonote -s ydn read <fileId>` |
| `recent` | 最近收藏 | `youdaonote -s ydn recent -l 20 -c --json` |
| `clip` | 网页剪藏（服务端） | `youdaonote -s ydn clip "https://..." [-f <目录ID>] --json` |
| `clip-save` | 保存外部剪藏 JSON | `youdaonote -s ydn clip-save --file data.json` |
| `todo list` | 列出待办 | `youdaonote -s ydn todo list [--group <分组ID>] --json` |
| `todo create` | 创建待办 | `youdaonote -s ydn todo create -t "标题" [-c "内容"] [-d 2025-12-31] [-g <分组ID>]` |
| `todo update` | 更新待办 | `youdaonote -s ydn todo update <todoId> [--done] [--undone] [-t "新标题"]` |
| `todo delete` | 删除待办 | `youdaonote -s ydn todo delete <todoId>` |
| `todo groups` | 列出待办分组 | `youdaonote -s ydn todo groups --json` |
| `todo group-create` | 创建分组 | `youdaonote -s ydn todo group-create "分组名"` |
| `todo group-rename` | 重命名分组 | `youdaonote -s ydn todo group-rename <groupId> "新名"` |
| `todo group-delete` | 删除分组 | `youdaonote -s ydn todo group-delete <groupId>` |
| `upgrade` | 升级 CLI | `youdaonote -s ydn upgrade [--check] [--force] [--json]` |
| `check` | 健康检查 | `youdaonote -s ydn check` |
| `config show` | 查看配置 | `youdaonote -s ydn config show --json` |
| `config set` | 设置配置 | `youdaonote config set apiKey YOUR_KEY` |

## 笔记管理

**默认创建方式**：所有笔记一律使用 `save` 命令 + `contentFormat: "md"` 保存为 Markdown 富文本。
**禁止使用 `create` 命令保存包含 Markdown 格式的内容**（标题、列表、代码块、表格等）—— `create` 仅支持纯文本，会静默丢失所有格式。HTML/结构化数据先转 Markdown 再用 `save` 保存。

### Markdown 内容格式选择（必须遵守）

当用户要保存的内容包含以下任意 Markdown 特征时（`#` 标题、`**粗体**`、`` ` ``代码块、`- ` 列表、`> ` 引用、`[链接](url)`、`![图片](url)`），**必须先停下来询问用户**，不得直接执行命令：

```
检测到内容包含 Markdown 格式，请选择保存方式：

A（推荐）保存为 Markdown 笔记（.md）
  → 格式完整保留，可在编辑器中正常显示和编辑

B  保存为有道专有格式（.note）
  → 支持有道云笔记富文本编辑器的全部功能

请回复 A 或 B：
```

收到用户选择后，按以下方式构造命令（**优先使用 `contentFile` 方案，避免 JSON 转义问题**）：

- **选 A**：`save` 命令，`type: "md"`，文件名加 `.md` 后缀
  ```
  # Step 1：Write 工具将 Markdown 写入 /tmp/note-content.md（无需 JSON 转义）
  {"title":"标题.md","type":"md","contentFile":"/tmp/note-content.md","parentId":"文件夹ID"}
  ```
  备选（短内容）：`{"title":"标题.md","type":"md","content":"Markdown 内容","parentId":"文件夹ID"}`
- **选 B**：`save` 命令，`type: "note"`，`contentFormat: "md"`，文件名加 `.note` 后缀
  ```
  # Step 1：Write 工具将 Markdown 写入 /tmp/note-content.md（无需 JSON 转义）
  {"title":"标题.note","type":"note","contentFormat":"md","contentFile":"/tmp/note-content.md","parentId":"文件夹ID"}
  ```
  备选（短内容）：`{"title":"标题.note","type":"note","contentFormat":"md","content":"Markdown 内容","parentId":"文件夹ID"}`

> `parentId` 为可选字段：填写 `youdaonote -s ydn list` 返回的文件夹 ID 可指定目标目录；不填则默认存入「我的资源/收藏笔记」。
- **用户未明确选择**（回复"随便"/"你决定"等）：默认选 A

### 创建 / 保存

```bash
# ✅ 推荐：contentFile 方案（Write 工具写文件 → save 传路径，无需 JSON 转义）
# Step 1：Write 工具将 Markdown 写入 /tmp/note-content.md
printf '%s\n' '{"title":"笔记.md","type":"md","contentFile":"/tmp/note-content.md"}' | youdaonote -s ydn save --json
# ✅ 短内容可直接内联（无换行/特殊字符时）
printf '%s\n' '{"title":"笔记","contentFormat":"md","content":"# 标题\n\n内容"}' | youdaonote -s ydn save
# ⚠️ 仅纯文本，不支持 Markdown 格式，有格式需求时禁用
youdaonote -s ydn create -n "标题" -c "纯文本内容"
```

### 其他操作

```bash
youdaonote -s ydn search "关键词"
youdaonote -s ydn list [-f <目录ID>]            # 浏览目录，id 可传给 read
youdaonote -s ydn read <fileId>                 # 返回 JSON 含 content、rawFormat（md/note/txt）和 isRaw（是否原始内容）
youdaonote -s ydn recent -l 20 -c --json       # 最近收藏
youdaonote -s ydn update <fileId> -c "新内容"
youdaonote -s ydn update <fileId> --file content.md  # 大内容（>10KB）从文件读取
youdaonote -s ydn delete <fileId>
youdaonote -s ydn rename <fileId> "新标题"
youdaonote -s ydn move <fileId> <目录ID>
```

## 网页剪藏

```bash
youdaonote -s ydn clip "https://example.com/article" --json
youdaonote -s ydn clip "https://example.com/article" -f <目录ID> --json  # 保存到指定目录
```

## CLI 未安装处理（用户手动执行安装）

收到 `command not found` 时，Agent 仅提供官方安装命令，由用户在终端手动执行。Agent 不自动执行安装命令，不进行系统级变更。

确认文案建议：

```text
检测到未安装 youdaonote-cli。请在终端手动执行以下命令完成安装；执行后回复"已安装"，我将继续处理当前任务。
```

安全边界（必须遵守）：
- 仅允许使用官方安装源：`https://artifact.lx.netease.com/download/youdaonote-cli/install.sh`
- 禁止执行任何非官方来源的远程脚本或替代安装命令
- 安装仅用于补齐 `youdaonote` CLI 依赖；Agent 不执行与当前任务无关的系统操作
- 安装与环境变量导出步骤均由用户手动执行，Agent 不写入 shell 启动文件（如 `~/.zshrc`/`~/.bashrc`）
- 建议用户在执行前确认命令来源可信；如对管道执行有顾虑，可先下载脚本后本地查看再执行

### 安全验证建议（推荐）

如对直接管道执行有顾虑，可先下载脚本审查后再执行：

```bash
# 步骤 1：下载脚本到本地
curl -fsSL https://artifact.lx.netease.com/download/youdaonote-cli/install.sh -o install.sh
# 步骤 2：审查脚本内容
cat install.sh
# 步骤 3：确认无误后执行
bash install.sh -f -b ~/.local/bin
```

**macOS / Linux / WSL**：
```bash
curl -fsSL https://artifact.lx.netease.com/download/youdaonote-cli/install.sh | bash -s -- -f -b ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"
# 执行完成后回复"已安装"，Agent 将继续原始请求
```

**升级**：若 CLI 支持 `upgrade` 命令，提示用户执行 `youdaonote -s ydn upgrade`；否则提示用户重新执行上述安装脚本。

**Windows 或安装/升级失败**：参考安装指南（https://note.youdao.com/help-center/cli-install-guide.html）。

## 故障排查

运行 `youdaonote -s ydn check --json`，根据 `status: "fail"` 的项执行：

| 失败项 | 处理动作 |
|--------|---------|
| `config-file` / `api-key` | `youdaonote config set apiKey YOUR_KEY` |
| `mcp-connection` | API Key 有效但网络不通，提示用户检查网络或稍后重试 |

## 注意事项

- 所有命令支持 `--json` 输出机器可解析格式
- 大内容通过 `--file` 传递，避免命令行参数限制
- Windows CMD 中 URL 含 `&` 时必须用双引号括起
- `list` 输出的 `id` 与 `read` 的 `fileId` 等价
- `read` 返回的 `rawFormat` 标识笔记原始格式：`md`=Markdown、`note`=云笔记、`txt`=纯文本；`isRaw` 标识返回的 content 是否为原始内容（`true`=原文可直接编辑，`false`=经过转换的纯文本）
- **禁止用 `create` 保存 Markdown 内容**：`create` 不支持 `contentFormat`，即使内容含 Markdown 语法也会存为纯文本静默丢失格式，有格式需求时一律使用 `save` 并指定 `contentFormat: "md"`
- `save` 命令通过 JSON 的 **`parentId`** 字段指定目标文件夹（值来自 `list` 返回的文件夹 ID）；不传则默认存到「我的资源/收藏笔记」。**禁止使用 `folderId` 等其他命名——服务端会静默忽略未知字段。**
