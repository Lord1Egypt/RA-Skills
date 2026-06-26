# Configuration

`monitor-tracker-runs.js` currently targets the Beijing tracker cron job by reading:

- Cron runs file: `/home/SENSETIME/zhangjiazhao/.openclaw/cron/runs/407511f7-5f9f-4a1e-aee9-c2e0764fb5e4.jsonl`
- Feishu config: `/home/SENSETIME/zhangjiazhao/.openclaw/workspace/skills/beijing-signed-price-tracker/projects.json`

The script sends a Feishu private message to `feishu.notifyUserOpenId` using `feishu.appId` and `feishu.appSecret`.

Current notification format is mobile-first and includes only:

- 最近一次执行时间
- 状态
- 详情

If you repoint this skill to a different cron job, update:

- `TARGET_JOB_ID`
- `TARGET_JOB_NAME`
- `RUNS_PATH`
- any config path assumptions
