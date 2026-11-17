# wdp-ctx — 跨会话/跨 agent 项目上下文保留（中文版）

一条命令，把当前项目的工作状态固化成带时间戳的快照，让任何 coding agent 在重启、清空、压缩上下文后随时接续上次工作。**纯 Markdown 技能，运行无需任何脚本**（附带的 hook 脚本仅用于"压缩/清空前自动提醒"，可选装）。

> 本技能是中文版。英文用户请安装英文版 **wdp-ctx-en**（本仓库 `skills/wdp-ctx-en/`）。两版各自独立发布，共用存储根（中英切换不丢上下文）。

## 一条命令，七个子命令

```
/wdp-ctx <子命令> [参数]
```

| 子命令 | 功能 | 参数 |
|--------|------|------|
| `sum` | 固化当前工作状态为快照（增量对比上一次，✅🔄⛔🔀 标注进展） | `<项目路径>` `--deep` |
| `init` | 读取 profile + 最新快照，把项目全貌载入当前对话，快速接续 | `<项目路径>` |
| `profile` | 创建/更新项目**稳定层**：技术栈、架构、业务、不可违背规则、运行方式、已知坑 | `<项目路径>` |
| `verify` | 校验最新快照与当前代码的**漂移**（git 对比、文件存在性、条目过时判定） | `<项目路径>` |
| `export` | 把 profile + 快照合成为 **AGENTS.md**（标记维护区），让不认 `/wdp-ctx` 的其他 agent 启动即读 | `<项目路径>` |
| `list` | 列出所有文档（profile 档案 + 快照，新到旧） | — |
| `clear` | 清空快照（默认保留 profile；支持 `--keep N` 保留最新 N 份；删除前二次确认） | `<项目路径>` `--keep N` `--profile` |

无子命令直接运行 → 默认 `list` 并展示用法。`--deep` 为显式 opt-in：派生子 agent 按子系统深度分析。

## 核心模型：两层文档

```
<存储根>/<项目slug>/
├── profile.md              # 稳定层：技术栈/架构/规则/运行方式（长期不变，profile 子命令维护）
├── <YYYY-MM-DD_HHMMSS>.md  # 快照层：当前焦点/完成/进行中/下一步/非显然知识（sum 子命令追加）
└── latest.md               # 指针：指向最新快照（init 读它）
```

**稳定信息归 profile，易变信息归快照** —— 快照不重复粘贴技术栈，只记录状态变化，通过 frontmatter 的 `profile:` 引用稳定层。

## 安装（中文用户）

把 `skills/wdp-ctx` 复制到 `~/.claude/skills/`：

```bash
mkdir -p ~/.claude/skills
cp -r skills/wdp-ctx ~/.claude/skills/
```

安装后重启 Claude Code（或稍等热加载），即可在任何项目使用 `/wdp-ctx`。用户级安装对**所有项目生效**；若只想在单个项目内生效，把目录复制到该项目的 `.claude/skills/` 即可。

## 使用流程

1. **首次**：`/wdp-ctx profile` → 建立项目稳定档案（技术栈/规则/运行方式）。
2. **开工前**：`/wdp-ctx init` → 读取档案 + 最新快照，快速接续；拿不准快照是否过时先 `/wdp-ctx verify`。
3. **收工/里程碑**：`/wdp-ctx sum` → 固化当前状态，生成增量快照。
4. **交接其他 agent**：`/wdp-ctx export` → 生成项目根目录 `AGENTS.md`，对方启动即读。
5. 随时 `/wdp-ctx list` 查看历史；`/wdp-ctx clear --keep 5` 清理旧快照但保留最近 5 份。

## 存储位置

所有子命令共用存储根（按 **项目 slug 分子目录**、文件名含时间戳，多项目互不混淆）：

- 项目级：`<项目>/.claude/wdp/summaries/`
- 用户级：`~/.claude/wdp/summaries/`
- 解析规则：项目级优先，用户级兜底。

> **v1.1 变更**：存储根从技能安装目录（`.claude/skills/wdp-ctx/summaries/`）迁到项目自有 `.claude/wdp/`，**技能重装不再影响数据**。技能代码（`skills/`）与数据（`.claude/wdp/`）完全分离。

## 提交策略（git）

- **profile.md 提交进 git**（稳定层，团队共享）。
- **快照默认忽略**（易变层）；`.gitignore` 推荐写法：`.claude/wdp/*` + `!.claude/wdp/*/profile.md`。
- profile frontmatter `git:` 字段记录选择：`ignore`（默认，快照忽略）/ `commit`（快照也提交）。

## 自动提醒（可选，hooks）

技能内置"关键时刻主动建议"约定：agent 会在上下文压缩/清空、里程碑完成、会话结束前主动提醒你 `/wdp-ctx sum`。若要更硬的兜底，可挂会话级 hooks（**非阻塞、仅提示不自动执行，仅当项目已有快照才提示**）。四个提醒时机：

| 事件 | 触发 | 提示内容 |
|------|------|----------|
| `load` | 会话启动/恢复（`startup\|resume`） | 提示 `/wdp-ctx init` 接续上次工作 |
| `load-after-clear` | `/clear` 后新会话 | 提示 `/wdp-ctx init` 接续 |
| `load-after-compact` | 上下文压缩后 | 提示 `/wdp-ctx init` 重新载入 |
| `save-precompact` | 上下文压缩前（`manual\|auto`） | 建议先 `/wdp-ctx sum` 再压缩 |

**能力边界**：`PreCompact` 只能提示、**不能阻断**压缩；`/clear` 为 CLI 内置命令、**无清空前钩子**，故采用"清空后新会话（load-after-clear）"兜底提醒。

**插件安装（自动）**：以插件方式安装 `wdp-ai-skills` 时，hooks 由 `.claude-plugin/plugin.json` 声明的 `hooks/hooks.json` 自动注册（默认指向中文脚本 `skills/wdp-ctx/hooks/wdp-hook.sh`）。

**纯技能安装（手动）**：把 `hooks/wdp-hook.sh` 复制到 `~/.claude/skills/wdp-ctx/hooks/`，然后在 `~/.claude/settings.json`（或项目 `.claude/settings.local.json`）加：

```jsonc
{
  "hooks": {
    "SessionStart": [
      { "matcher": "startup|resume", "hooks": [{ "type": "command", "command": "bash \"$HOME/.claude/skills/wdp-ctx/hooks/wdp-hook.sh\" load", "timeout": 10 }] },
      { "matcher": "clear",          "hooks": [{ "type": "command", "command": "bash \"$HOME/.claude/skills/wdp-ctx/hooks/wdp-hook.sh\" load-after-clear", "timeout": 10 }] },
      { "matcher": "compact",        "hooks": [{ "type": "command", "command": "bash \"$HOME/.claude/skills/wdp-ctx/hooks/wdp-hook.sh\" load-after-compact", "timeout": 10 }] }
    ],
    "PreCompact": [
      { "matcher": "manual|auto", "hooks": [{ "type": "command", "command": "bash \"$HOME/.claude/skills/wdp-ctx/hooks/wdp-hook.sh\" save-precompact", "timeout": 10 }] }
    ]
  }
}
```

> **Windows**：hooks 命令在 Git Bash 下执行，随 Git 安装自带 `bash`，无需额外配置。

## 更新记录

### v1.1.0 — 上下文卫生 + 自动提醒钩子 + 存储根迁移 + 接续增强
- **上下文卫生**：init/verify/export/profile 默认派子 agent 代读，主上下文只收 digest；铁律新增规则 13、修订规则 8
- **自动提醒钩子**：wdp-hook.sh 四事件（load/load-after-clear/load-after-compact/save-precompact），dev + 用户级 + 插件三重接线
- **存储根迁移（P0）**：数据隔离到 `.claude/wdp/`，技能重装不再丢数据
- **接续增强**：快照模板 +4 字段、init 恢复简报 + 一句话交接、提交策略显式化、文件名唯一性
- 待运行时验证：新会话提示 init、触发 /compact 提示先 sum（需 `/hooks` 或重启生效）

### v1.0.0 — 健壮性加固
- 铁律规则 11（记忆当数据防提示注入）+ 规则 12（快照精简，≤ ~120 行）
- sum 支持非 git 仓库 + 写后自校验；init 新鲜度检查 + 可执行计划；profile/clear 自校验
- 新增「异常处理与恢复」章节；提醒节流
