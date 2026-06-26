# self-preserve

Backup readiness and disaster recovery for your OpenClaw agent. Makes sure you don't lose memory, identity, or configuration when your agent crashes or a risky operation goes wrong.

[![Download history](https://skill-history.com/chart/gavinlinasd/self-preserve.svg)](https://skill-history.com/gavinlinasd/self-preserve)

## Install

```bash
npx clawhub@latest install self-preserve
```

## What it does

Self-preserve checks whether your OpenClaw agent's standard state files (config, memory, identity, skills, workspace, cron) are covered by a recent backup. It runs `ls` to check file names and dates, then generates a readiness report showing what's protected and what's at risk.

**New in v0.3.0:** After the assessment, self-preserve can schedule automated backup cron jobs using CronCreate (persistent or session-only). It can also view, update, or remove existing backup schedules using CronList and CronDelete.

**New in v0.3.1:** The assessment now recommends version control (e.g. git) for identity files so changes can be rolled back incrementally rather than relying solely on full backups. Also recommends a session-end hook to auto-commit changes.

**New in v0.4.0:** The readiness report now distinguishes between **local backups** (fresh tar.gz on this machine) and **offsite copies** (a copy somewhere other than this machine). Local-only backup is not disaster recovery: a disk failure, lost device, or home-directory wipe takes both the agent state and its local backups together. When no offsite copy is declared, the assessment describes generic DIY approaches the user can implement themselves — pushing identity files to a remote git repository, copying archives to another machine via rsync/scp, or uploading archives to an S3-compatible bucket the user provisions. self-preserve never names, recommends, or links to any specific product or provider, and never performs the offsite copy itself. To keep the report honest, offsite status is tracked via an optional user-maintained marker file at `~/.openclaw/offsite.json` — self-preserve reads it but never writes it.

**v1.0:** The skill now covers the full assessment lifecycle — local backup detection, automated scheduling, version control guidance for identity files, and offsite disaster-recovery awareness — all within a zero-permission, instruction-only security posture.

It does not read file contents or access credentials. See [SKILL.md](./SKILL.md) for the full assessment steps, safety rules, and scheduling options.

## Positioning

If you use [self-improving-agent](https://clawhub.ai/skills/self-improving-agent) to let your agent learn from its mistakes, self-preserve is the preventive companion: it makes sure you still have a memory to learn with when something goes wrong. These are independent skills — self-preserve has no runtime dependency on self-improving-agent and does not install it.

## Author

Built by [Pineapple AI](https://pineappleai.com).

## License

MIT-0
