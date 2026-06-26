# Report Format

Only use this template AFTER Phase 3 (changelog) and Phase 4 (risk) are complete.

## Template

```
🔄 Smart Updater — 升级扫描报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 扫描了 {{total_assets}} 个资产，发现 {{update_count}} 个可用更新：

{{for each update, grouped by risk:}}

🟢 推荐升级（patch bugfix）
  N. {{name}} {{current}} → {{latest}}
     📝 {{changelog_summary — REQUIRED, from Phase 3}}
     🔗 {{changelog_source — REQUIRED, URL or command used}}
     ⚠️ 风险：低

🟡 建议升级（minor/feature）
  N. {{name}} {{current}} → {{latest}}
     📝 {{changelog_summary — REQUIRED, from Phase 3}}
     🔗 {{changelog_source — REQUIRED, URL or command used}}
     ⚠️ 风险：中

🔴 需确认（major/breaking）
  N. {{name}} {{current}} → {{latest}}
     📝 {{changelog_summary — REQUIRED, from Phase 3}}
     🔗 {{changelog_source — REQUIRED, URL or command used}}
     ⚠️ 风险：高（{{breaking_change_detail}}）

🟠 需人工审查（changelog 不可用）
  N. {{name}} {{current}} → {{latest}}
     📝 changelog 获取失败：{{reason}}
     ⚠️ 风险：未知

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
回复编号选择升级，如 "1 2" 升级前两个
回复 "all" 全部升级
回复 "skip" 跳过本次
回复 "detail N" 查看完整 changelog
```

## Required Fields

Every update entry MUST include:
- `changelog_summary` — from Phase 3 changelog fetch (NOT invented)
- `changelog_source` — the URL or command used to obtain the changelog
- `risk_level` — from Phase 4 risk assessment

If `changelog_summary` is empty, you did not complete Phase 3. Go back.
