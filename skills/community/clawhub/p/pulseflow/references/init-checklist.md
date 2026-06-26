# Init Checklist

Use this checklist when installing the system into a new vault or workspace.

1. Create `todo/`, `todo/history/`, `todo/system/`
2. Create `todo/NOW.md` from `references/now-template.md`
3. Create current month archive file from `references/history-template.md`
4. Create `todo/system/config.json` from `references/config-template.json`
5. Create `todo/system/sync-state.json` from `references/sync-state-template.json`
6. Create empty today log files for each enabled agent:
   - `<reportsDir>/<agent>-ai-log-YYYY-MM-DD.jsonl`
7. Set each agent's `agentsFilePath` in config and run `scripts/install_agent_log_rules.js`
8. Confirm each agent's `AGENTS.md` contains the managed AI log rule block
9. Update the coordinator heartbeat to run `scripts/sync_ai_done.js`
10. Run one manual sync test
11. Confirm `NOW.md` and `sync-state.json` both update correctly
12. Optional: if the installation wants scheduled summaries, fill `notifications.summaryCrons` and run `scripts/install_summary_crons.js`
