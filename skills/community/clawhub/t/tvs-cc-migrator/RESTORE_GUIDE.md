# Claude Code 配置恢复指南

这是一个 Claude Code 配置备份包。请让 Claude 读取本文件，它会引导你完成恢复。

## 恢复方式

在新机器上打开 Claude Code，对 Claude 说：

> 帮我恢复 Claude Code 配置，请先读取这个文件：<本文件的绝对路径>

Claude 会按照下面的指令自动完成恢复。

---

## 以下内容供 Claude 阅读

### 你的任务

你正在帮用户恢复 Claude Code 配置。备份包内有一个 `manifest.json`，它描述了所有需要恢复的配置项。数量和内容因用户不同而不同，你需要完全基于 manifest.json 来理解和操作，不要做任何假定。

### 第一步：读取 manifest.json

读取本文件同目录下的 `manifest.json`，了解：
- `summary` — 备份的总文件数和配置项数
- `items` — 每个配置项的名称、类型、路径、描述、文件列表
- `source_machine` / `source_platform` — 来源信息，供参考

### 第二步：解析路径

manifest.json 中的 `target` 字段使用 `<claude-home>` 占位符，根据当前平台解析为实际路径：
- **Mac / Linux**: `~/.claude`（即 `$HOME/.claude`）
- **Windows**: `%USERPROFILE%\.claude`（即 `C:\Users\用户名\.claude`）

### 第三步：展示配置清单并询问恢复策略

遍历 manifest.json 的 `items` 数组，向用户展示所有配置项。格式：

```
检测到以下配置（来自 <source_machine>，备份于 <created_at>）：

  [编号]. [name] — [description]（[files.length] 个文件）
  ...

共 [summary.total_items] 项配置，[summary.total_files] 个文件。

请选择恢复策略：
1. 全量覆盖 — 用备份内容替换本机配置（已有配置会被覆盖）
2. 追加合并 — 仅添加本机没有的配置，已有的保持不动

是否有不需要恢复的项？请告诉我编号。
```

等待用户选择后再继续。

### 第四步：执行恢复

根据用户选择的策略，按 manifest.json 中每个 item 的 `type` 字段决定恢复方式：

#### type: direct_copy

将备份包内 `source` 路径的文件/目录复制到 `target` 路径。

- **全量覆盖**：直接覆盖目标路径
- **追加合并**：逐个文件检查，目标文件不存在时才复制，已存在的跳过

操作前确保目标目录存在，不存在则创建。

#### type: merge_settings

这是 `settings.json` 的处理方式，需要特殊对待：

1. 读取备份的 `settings.json` 和本机已有的 `settings.json`（如果有）
2. 检查 `sensitive_fields` 字段列出的敏感项
3. 同时扫描 `env` 对象中所有包含 `TOKEN`、`SECRET`、`KEY`、`PASSWORD`、`CREDENTIAL`、`AUTH` 的键
4. 如果这些字段已有值，清空它们并记录
5. **全量覆盖**：用处理后的备份 settings 替换本机 settings
6. **追加合并**：仅补充本机 settings 中缺失的键，已有的键不修改
7. 完成后提醒用户手动配置被清空的敏感字段

#### type: reinstall

这些是通过市场安装的插件，不直接复制文件。

1. 读取 `reinstall_commands` 字段
2. 向用户展示安装命令列表
3. 询问是否执行安装
4. 用户确认后逐条执行

### 第五步：验证

恢复完成后，检查 `<claude-home>` 目录结构，确认配置已就位。向用户汇报恢复结果，列出已恢复和跳过的项目。
