# x-skill-updater

OpenClaw Skill 更新检查与升级管理工具。

> `<OPENCLAW_HOME>` 是你的 OpenClaw 配置根目录，通常为 `~/.openclaw`。以下所有路径中的 `<OPENCLAW_HOME>` 均需替换为你实际安装的路径。

## 功能

- 自动扫描 `<OPENCLAW_HOME>/skills/` 和 `<OPENCLAW_HOME>/workspace-*/skills/` 下所有 skill
- 全量字段核对：`_meta.json`（ownerId / slug / version / publishedAt）+ `SKILL.md`（author / slug / homepage / metadata）
- 不降级：本地版本高于官频时跳过
- 征得用户同意后再执行升级

## 前置要求

- OpenClaw 已安装
- `skillhub` CLI（用于 skillhub 来源升级）
- `clawhub` CLI（用于 clawhub 来源升级）

## 安装

```bash
# 安装到全局 skills 目录（标准方式）
cp -r x-skill-updater <OPENCLAW_HOME>/skills/

# 安装到 workspace skills 目录
cp -r x-skill-updater <OPENCLAW_HOME>/workspace-<id>/skills/
```

## 使用

```bash
# 检查更新（手动触发）
python3 <OPENCLAW_HOME>/skills/x-skill-updater/scripts/check.py

# 执行升级（征得同意后）
python3 <OPENCLAW_HOME>/skills/x-skill-updater/scripts/upgrade.py <slug>
python3 <OPENCLAW_HOME>/skills/x-skill-updater/scripts/upgrade.py --all

# 补充未知 skill 来源
python3 <OPENCLAW_HOME>/skills/x-skill-updater/scripts/reply.py "skill名 → clawhub"
```

## 定时自动检查（可选）

通过 OpenClaw cron 配置（将 `<OPENCLAW_HOME>` 替换为实际路径）：

```json
{
  "name": "skill-updater-weekly",
  "schedule": { "kind": "cron", "expr": "0 9 * * 1", "tz": "Asia/Shanghai" },
  "payload": { "kind": "agentTurn", "message": "执行 skill 更新检查：python3 <OPENCLAW_HOME>/skills/x-skill-updater/scripts/check.py" },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce" },
  "enabled": true
}
```

## 数据文件

- `data/skill-sources.json` — skill 来源配置（首次使用前根据实际安装的 skill 补全）
- `data/last-report.md` — 上次检查报告
- `data/pending-sources.json` — 待确认来源的 skill 列表

---

License: MIT
