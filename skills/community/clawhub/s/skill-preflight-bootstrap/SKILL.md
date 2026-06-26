---
name: skill-preflight-bootstrap
description: 为新仓库一键初始化“任务前先查技能”的工作流。适用于初始化技能预检新仓库、给新仓库装技能工作流、迁移 skill preflight、把当前流程封装到另一个仓库，或把技能预检、项目级 hooks、`.learnings/` 和团队使用说明快速落到目标仓库时。
---

# 新仓库技能预检初始化

把“先查技能，再执行任务”的仓库级能力一键落到目标目录。

## 什么时候用

在下面这些场景触发：

- 你想把当前仓库的技能预检流程迁移到另一个新仓库
- 你希望新仓库默认带上 `skill-preflight.py`
- 你需要同时生成项目级 `.codex/settings.json` / `.claude/settings.json`
- 你希望顺手创建 `.learnings/` 和团队说明文档

## 快速使用

### 1. 先决定目标目录

目标目录通常是一个新的或尚未配置这套流程的仓库。

### 2. 执行 bootstrap 脚本

从本 skill 根目录运行：

```bash
python3 scripts/bootstrap-skill-preflight.py /path/to/target-repo
```

如果只想先看将要写入什么：

```bash
python3 scripts/bootstrap-skill-preflight.py /path/to/target-repo --dry-run
```

如果目标仓库里已有同名模板文件，且你确认要覆盖：

```bash
python3 scripts/bootstrap-skill-preflight.py /path/to/target-repo --force
```

## 它会写什么

- `scripts/skill-preflight.py`
- `scripts/hooks/skill-preflight-reminder.sh`
- `scripts/hooks/error-learning-reminder.sh`
- `.codex/settings.json`
- `.claude/settings.json`
- `.learnings/LEARNINGS.md`
- `.learnings/ERRORS.md`
- `.learnings/FEATURE_REQUESTS.md`
- `docs/skill-preflight-usage.md`
- `AGENTS.md` 中的技能预检片段

## 使用原则

- 默认只写项目级配置，不碰用户全局环境
- 已存在的 `AGENTS.md` 只追加片段，不整文件覆盖
- 已存在的设置文件会合并 hooks，而不是粗暴覆盖
- 默认跳过已存在的模板文件；只有 `--force` 才覆盖

## 验证

落地后建议至少做三步检查：

1. 验证 JSON：
   - `python3 -m json.tool /path/to/target-repo/.codex/settings.json`
   - `python3 -m json.tool /path/to/target-repo/.claude/settings.json`
2. 验证预检脚本：
   - `python3 /path/to/target-repo/scripts/skill-preflight.py "react performance"`
3. 检查 `AGENTS.md` 是否只追加一次技能预检片段

## 参考

- 示例和验收方式见 `references/examples.md`

## 注意

如果目标仓库的 `AGENTS.md` 或设置文件有强烈的项目定制逻辑，先用 `--dry-run` 看计划，再决定是否执行。
