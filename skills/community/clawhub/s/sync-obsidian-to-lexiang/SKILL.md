---
name: sync-obsidian-to-lexiang
description: >-
  Obsidian vault 到腾讯乐享知识库的单向全量或增量同步工具。保留目录结构，
  同步 Markdown 图文和独立附件。Markdown 页面统一复用
  upload-markdown-to-lexiang。用户提到同步 Obsidian 到乐享、笔记同步知识库时使用。
version: "2.1.1"
category: productivity
tags: obsidian, lexiang, sync, markdown, chinese, knowledge-base
agent_created: true
requires:
  skills:
    - name: upload-markdown-to-lexiang
      version: ">=1.3.1,<2.0.0"
---

# Sync Obsidian to Lexiang

将 Obsidian vault 单向同步到腾讯乐享，支持全量、增量、中断恢复和冲突保护。

## 能力边界

本 Skill 负责：

- 扫描 vault 和目录树
- content hash 增量判断
- manifest、文件锁和中断恢复
- 冲突策略和目的端移动检测
- 独立附件上传
- 把 Obsidian wikilink 转为临时标准 Markdown 包

`upload-markdown-to-lexiang` 负责：

- Markdown page 创建和覆盖
- 本地内嵌图片
- 公式、表格和图文顺序
- 上传前预检和上传后对账
- 乐享个人凭证

禁止在本 Skill 的 `lexiang_api.py` 中恢复 Markdown page 上传实现。

## 依赖定位

不得写死 WorkBuddy、OpenClaw 或其他 Agent 路径。按以下顺序定位公共 Skill：

1. `LEXIANG_UPLOADER_HOME`
2. 本 Skill 所在 skills 根目录的同级 `upload-markdown-to-lexiang`
3. 当前 Agent 暴露的已安装 Skill
4. 当前平台 Skill 管理器默认位置

缺失时安装到本 Skill 所在的同一个 skills 根目录。

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" --version
# cli_api == "1"
python3 "<uploader-root>/scripts/lexiang_upload.py" auth status --check
```

首次凭证配置：

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" auth login
```

个人凭证从 <https://lexiangla.com/ai/claw> 获取。

默认情况下，目录、探活和独立附件仍复用 Agent 乐享连接器。显式选择
`--lexiang-profile` 或 `--lexiang-credential-file` 后，Markdown、目录、
探活和独立附件统一使用该 ai/claw 个人凭证。Markdown 内容不会进入对话上下文。

## 标准使用

首次建议 dry-run：

```bash
python3 scripts/sync.py \
  --mode full \
  --target-space-id <SPACE_ID> \
  --target-folder-id <FOLDER_ID> \
  --vault-path "<VAULT>" \
  --dry-run
```

正式同步：

```bash
python3 scripts/sync.py \
  --mode incremental \
  --target-space-id <SPACE_ID> \
  --target-folder-id <FOLDER_ID> \
  --vault-path "<VAULT>"
```

大批量后台执行：

```bash
python3 scripts/sync.py ... --lexiang-profile obsidian-sync --background
python3 scripts/sync.py --status --vault-path "<VAULT>"
```

命名 profile 位于 `~/.config/lexiang-upload/profiles/<name>.json`；
`default` 对应 `~/.config/lexiang-upload/credentials.json`。也可直接传
`--lexiang-credential-file <PATH>`，两者不能同时使用。命令行选择会写入
vault 的 config（只保存 profile 名或路径，不保存 token），后续定时任务可复用。
若 config 未设置，则考虑 `LEXIANG_UPLOAD_CREDENTIALS` /
`LEXIANG_UPLOAD_PROFILE`；都未设置时保持原连接器默认行为。

stdout 只输出 JSON 摘要和报告路径；进度写 stderr 或 `progress.json`。

## 参数

| 参数 | 说明 | 默认 |
|---|---|---|
| `--mode` | `full` / `incremental` | 首次 full，之后 incremental |
| `--target-space-id` | 目标知识库 | 必填 |
| `--target-folder-id` | 目标目录 | 知识库根目录 |
| `--vault-path` | Obsidian vault | 自动检测 |
| `--source-dirs` | 指定同步目录 | 全部 |
| `--conflict-strategy` | `lexiang_wins` / `obsidian_wins` | `lexiang_wins` |
| `--respect-move` | 尊重乐享侧移动 | true |
| `--lexiang-profile` | 命名个人凭证 profile | config / 环境 / 未设置 |
| `--lexiang-credential-file` | 个人凭证 JSON 路径，与 profile 互斥 | config / 环境 / 未设置 |
| `--dry-run` | 仅预览 | false |

## 同步规则

### Markdown

1. 将 wikilink 和 Obsidian 图片引用转换为标准 Markdown。
2. 本地图片复制到一次性临时工作包。
3. 创建时调用公共 CLI 的 `--parent-id`。
4. 更新时调用公共 CLI 的 `--entry-id`。
5. 只有 `verified=true` 后才写入 manifest。

临时工作包在单篇完成后自动删除，不是第二份上传源码。

### 独立文件

PDF、Office、独立图片、音视频等作为 file entry 上传。它们不调用公共 Markdown 上传器。

### 增量和中断恢复

- 每项成功后立即保存 manifest。
- 内容 hash 未变化则跳过。
- entry 探活失败时保留映射，下次重试。
- manifest 丢失时先查询同名同类型 entry，避免重复创建。
- 两个进程同时同步时由 `.sync.lock` 阻止并发。

### 冲突

- `lexiang_wins`：乐享在上次同步后被独立编辑则跳过覆盖。
- `obsidian_wins`：Obsidian 变更始终覆盖。
- `respect_move=true`：目的端移动后继续更新原 entry。

## 状态文件

```text
{vault}/.obsidian/plugins/sync-obsidian-to-lexiang/
├── config.json
├── manifest.json
├── .sync.lock
├── progress.json
└── reports/
```

## 代码边界

| 文件 | 职责 |
|---|---|
| `scripts/sync.py` | 扫描、调度、临时 Markdown 工作包、调用公共 CLI |
| `scripts/lexiang_api.py` | 目录、探活和独立附件，不含 Markdown page 上传 |
| `scripts/converter.py` | Obsidian 语法和附件解析 |
| `scripts/manifest.py` | 配置与 manifest |
| `scripts/report.py` | 同步报告 |
| `scripts/progress.py` | 后台进度 |
| `scripts/test_sync.py` | 离线回归测试 |

## 测试

```bash
python3 scripts/test_sync.py
```

默认测试必须离线，不得在真实知识库创建目录或文档。

公共上传行为有问题时，只修改 `upload-markdown-to-lexiang` 并补它的测试；
本 Skill 只测试临时工作包、CLI 调用、manifest 和同步调度。
