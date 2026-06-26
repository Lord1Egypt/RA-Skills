# skills-audit 脚本说明（v1.5.0）

目标：在不执行任何 skill 代码的前提下，对 `workspace/skills` 做**静态审计**，并把结果写入本地 **append-only NDJSON**。

## 环境要求

- Python ≥ 3.9，无第三方依赖（仅使用标准库）
- git（用于 content diff 快照）
- 依赖声明见 `requirements.txt`

## 输出（固定位置）

```
~/.openclaw/skills-audit/
├── logs.ndjson          # 审计日志（追加写）
├── state.json           # 扫描状态快照（用于 diff）
├── baseline.json        # 已审核 skill 基线
└── snapshots/           # git repo（content diff 快照）
```

日志字段以 `skills-audit/log-template.json` 为准。
通知模板见 `templates/notify.txt`。

## 奇安信情报查询

- 不再上传整个 skill 压缩包到奇安信平台
- 改为：对 **整个 `workspace/skills` 目录** 生成稳定 MD5，使用 token 查询奇安信 SafeSkill 情报
- 配置文件：`config/intelligent.json`
- 默认 `enabled` 为 `false`
- 默认 `token` 为空；用户下载后如需启用再自行填写
- 当功能关闭、`token` 为空或查询失败时：自动跳过远程情报，仅执行本地静态扫描

示例配置：

```json
{
  "token": "",
  "base_url": "https://safeskill.qianxin.com",
  "enabled": false,
  "mode": "md5-query"
}
```

## 主要脚本

### skills_audit.py

子命令：

- `init` — 初始化 logs/state/baseline/snapshots
- `scan` — 扫描 `workspace/skills`，对比 state 发现新增/变更/删除，
  计算文件级 diff，提交 git 快照，追加写审计日志
- `approve` — 将 skill 标记为已审核（写入 baseline）
  - `--skill <name>` 审核单个
  - `--all` 批量审核所有
- `baseline` — 管理基线
  - `--list` 列出已审核 skill
  - `--revoke --skill <name>` 撤销审核

### skills_watch_and_notify.py

面向"监控推送"的消息生成脚本：
- 有变化时输出格式化通知文本（从 `templates/notify.txt` 读取模板）
- 无变化则不输出（便于 cron 实现"无变化不发"）
- 已审核（baseline approved）且未变更的 skill 不会出现在通知中
- 支持分层展示（文件数少展开，文件数多折叠 + 警告）

## 常用命令

初始化：

```bash
python3 skills/skills-audit/scripts/skills_audit.py init --workspace /root/.openclaw/workspace
```

手动扫描：

```bash
python3 skills/skills-audit/scripts/skills_audit.py scan --workspace /root/.openclaw/workspace --who user --channel local
```

审核 skill（写入基线）：

```bash
python3 skills/skills-audit/scripts/skills_audit.py approve --skill weather --workspace /root/.openclaw/workspace
python3 skills/skills-audit/scripts/skills_audit.py approve --all --workspace /root/.openclaw/workspace
```

查看/撤销基线：

```bash
python3 skills/skills-audit/scripts/skills_audit.py baseline --list
python3 skills/skills-audit/scripts/skills_audit.py baseline --revoke --skill weather
```

查看 content diff：

```bash
git -C ~/.openclaw/skills-audit/snapshots diff HEAD~1 HEAD
git -C ~/.openclaw/skills-audit/snapshots diff HEAD~1 HEAD -- skills/weather/
git -C ~/.openclaw/skills-audit/snapshots log --oneline
```

监控通知（由 cron 定时执行）：

```bash
python3 skills/skills-audit/scripts/skills_watch_and_notify.py --workspace /root/.openclaw/workspace
```

推荐由助手或运维使用 `openclaw cron add` / `openclaw cron edit` 来创建定时任务。
