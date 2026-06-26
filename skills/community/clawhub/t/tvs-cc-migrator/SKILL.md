---
name: tvs-cc-migrator
description: Claude Code 配置迁移工具。备份和恢复 ~/.claude/ 下的所有配置（CLAUDE.md、rules、skills、commands、agents、自定义插件、settings.json 等）。当用户提到备份配置、迁移 Claude Code、导出设置、恢复配置、换电脑等场景时使用此 skill。
---

# CC Migrator — Claude Code 配置迁移

将本机的 Claude Code 配置打包备份，并在新机器上通过 Claude 智能恢复。

## 备份流程

备份分两步：**先扫描，再打包**。不要直接打包，因为用户可能有敏感信息需要先确认。

### 第一步：扫描检测

运行扫描命令，检测 `~/.claude/` 下所有可迁移的配置：

```bash
node <skill-path>/scripts/backup.mjs --scan
```

脚本会输出一份 JSON 报告，包含所有检测到的配置项。每项包含：
- `id` — 唯一标识，后续用于排除
- `name` — 显示名称
- `description` — 用途说明
- `file_count` — 文件数量
- `contains_sensitive` — 是否包含敏感信息
- `sensitive_fields` — 具体哪些字段是敏感的（仅 settings.json）

### 第二步：向用户展示并确认

读取扫描报告后，向用户展示检测到的所有配置：

```
检测到以下 Claude Code 配置：

  [编号] [名称] — [描述]（[文件数] 个文件）
  ...

以下配置包含敏感信息：
  - settings.json 中的 env.ANTHROPIC_AUTH_TOKEN（有值）
  - settings.json 中的 env.ANTHROPIC_BASE_URL（有值）

请确认：
1. 以上配置是否全部需要备份？如果有不需要的，请告诉我编号或名称
2. 敏感信息如何处理？
   a. 清空敏感字段后备份（推荐，恢复时需手动填写）
   b. 保留原值备份（注意：备份包中会包含密钥等敏感数据）
   c. 跳过 settings.json 不备份
```

等待用户确认后再继续。

### 第三步：执行备份

根据用户的选择构造命令：

```bash
# 备份所有（清空敏感字段）
node <skill-path>/scripts/backup.mjs [output-dir] --exclude=settings_sensitive

# 排除某些配置
node <skill-path>/scripts/backup.mjs [output-dir] --exclude=plugin_docx,agents

# 保留敏感字段原值
node <skill-path>/scripts/backup.mjs [output-dir]
```

- `output-dir` 可选，默认输出到 `~/Desktop/cc-backup-<date>/`
- `--exclude=id1,id2` 排除指定配置项（id 来自扫描报告）
- `--exclude=settings_sensitive` 特殊标记：保留 settings.json 但清空敏感字段
- 跨平台支持：Mac / Linux / Windows（Windows 下打包为 .zip）

备份完成后告知用户备份包路径和内容摘要。

## 恢复流程

恢复由 Claude 完成，不是脚本自动执行。这是因为恢复需要人为决策（覆盖 vs 追加）和敏感信息处理。

新机器上的用户只需让 Claude 读取备份包中的 `RESTORE_GUIDE.md`，Claude 即可按指引完成恢复。

### 恢复步骤概要

1. **解压备份包**：用户提供备份包路径，解压
2. **读取 manifest.json**：理解备份内容的完整结构
3. **展示配置清单**：列出所有备份项（名称、描述、文件数），完全基于 manifest.json 动态生成，不做任何假定
4. **询问恢复策略**：

向用户确认：

> 请选择恢复策略：
> 1. **全量覆盖** — 用备份内容完全替换本机配置（已有配置会被覆盖）
> 2. **追加合并** — 仅添加本机没有的配置，已有的不动

5. **逐项恢复**：根据策略和 manifest.json 中每项的 `type` 执行恢复

### 恢复细节

根据 manifest.json 中每个条目的 `type` 字段决定恢复方式：

| type | 全量覆盖 | 追加合并 |
|------|----------|----------|
| `direct_copy` | 直接覆盖目标路径 | 目标文件不存在时才复制 |
| `merge_settings` | 合并 JSON 结构，清空敏感字段后写入，提示用户填写 | 仅补充缺失的键，不修改已有键 |
| `reinstall` | 输出安装命令列表，让用户执行 | 仅列出本机未安装的 |

### 路径解析

manifest.json 中的路径使用 `<claude-home>` 占位符，恢复时根据当前平台解析：
- **Mac / Linux**: `~/.claude`
- **Windows**: `%USERPROFILE%\.claude`

### settings.json 特殊处理

settings.json 中的敏感信息由 manifest.json 的 `sensitive_fields` 字段标记。恢复时：
- 检查这些字段是否有值，如果已被清空则提醒用户手动配置
- 同时扫描 `env` 对象中所有包含 `TOKEN`、`SECRET`、`KEY`、`PASSWORD`、`CREDENTIAL`、`AUTH` 的键
- 恢复时保留结构（如 `enabledPlugins`、`extraKnownMarketplaces`），仅处理敏感值

### 市场插件处理

manifest.json 中 `type: "reinstall"` 的条目是市场插件，不直接复制文件。读取 `reinstall_commands` 字段，向用户展示安装命令列表，询问是否执行。

## manifest.json 结构说明

```json
{
  "version": "1.0",
  "created_at": "ISO 时间戳",
  "source_machine": "来源机器名",
  "source_user": "用户名",
  "source_platform": "darwin | linux | win32",
  "summary": {
    "total_files": "总文件数",
    "total_items": "配置项数"
  },
  "items": [
    {
      "name": "显示名称",
      "type": "direct_copy | merge_settings | reinstall",
      "source": "备份包内的相对路径",
      "target": "恢复到的目标路径（使用 <claude-home> 占位符）",
      "description": "用途说明",
      "files": ["文件列表"],
      "sensitive_fields": ["仅 merge_settings 类型"],
      "reinstall_commands": ["仅 reinstall 类型"]
    }
  ]
}
```

Claude 读取 manifest.json 后应能完整理解：
- 有哪些配置需要恢复（数量由 manifest 决定，不做假定）
- 每项配置的用途
- 如何恢复（直接复制 / 合并 / 重装）
- 恢复到哪个路径
