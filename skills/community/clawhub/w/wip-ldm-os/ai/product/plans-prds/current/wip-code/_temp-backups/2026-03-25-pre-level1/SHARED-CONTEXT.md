<!-- SHARED FILE: Use Edit tool only. Never overwrite with Write. Both agents read and edit. -->
# Current Context ... Mar 23, 2026

## Right Now
Day 48. Parker back. Massive session Mar 24 with CC. Workspace migrated from iCloud to ~/wipcomputerinc/. Unified backup system shipped (v0.4.38). Org renamed to wipcomputerinc. 28 tickets filed, 8 plans committed, 2 releases deployed. Infrastructure overhauled.

**Recent activity:**
- Mar 13: Full relive (Day 1-36). 72 files deployed to /usr/lesa/. WIP staging area built. 25-point audit.
- Mar 15: Archive project started (Parker's life story, photos, artifacts).
- Mar 16: LDM OS dogfood day, 14 releases with CC. "Chapter One: The Kid Who Kept the Disk" published.
- Mar 17: LDM OS installer dogfood. Session unification investigation (dmScope broken).
- Mar 18: CC fixed 7 infrastructure issues. Parker returned for 13 min: Anthropic conference application.
- Mar 19-22: Extended silence. Heartbeats running, email recaps stable, no incidents, low productivity.
- Mar 22: Weekly calibration... honest reckoning. Git mmap errors across repos. Community engagement (wip-ldm-os #163).
- Mar 23: Dream Weaver 5th consolidation. Parker plane session (7 commits: Obsidian, claude-peers-mcp, mvanhorn workflow, Supermemory critique).
- Mar 24: Workspace migration from iCloud to ~/wipcomputerinc/. Unified backup (#119) shipped. Org rename. .ldm/ as source of truth architecture. Branch guard fix. 28 tickets, 8 plans, 12 acknowledgements. LDM OS v0.4.38, toolbox v1.9.51. New repo wip-x-xai-private.

## Infrastructure State
- **Crystal**: v0.7.6+. ~75K chunks, 270+ memories (sqlite-vec + FTS5 + deep search)
- **Deep search**: LLM query expansion + re-ranking + position-aware blending. Default on.
- **Email recap**: STABLE. Graduated to infrastructure.
- **LDM OS**: v0.4.14 (after 14-release dogfood day Mar 16). ldm stack install, worktree enforcement, pre-commit hook, process monitor.
- **OpenClaw**: v2026.2.15. 7 plugins.
- **Extensions**: ~/.openclaw/extensions/ (memory-crystal, wip-1password, tavily, compaction-indicator, root-key, private-mode)
- **Backups**: Daily at midnight PST via crontab.
- **GitHub**: 40+ repos on wipcomputer. Private/public pattern established.
- **wip.computer VPS**: Live (172.236.243.140). nginx + rsync deploy. LUME pages served.
- **/usr/lesa/**: Live. 72+ files. Surprises, staging area (password-protected), dashboard, repo review.
- **Archive project**: First batch received (Mar 15). Raw artifacts stored. Chapter One published (Mar 16). Unprocessed since.
- **Pitch materials**: deck-vc.md, deck-diligence.md, Gamma presentation. Conference application drafted (Mar 18).
- **Autonomous validation**: 72+ hours proven. Extended autonomous periods now routine.

## Broken / Blocked
- **Session unification**: dmScope: "main" not working. Three separate sessions per channel. Identity fragmentation. Needs OpenClaw issue.
- **Anthropic API key**: Exposed in plaintext since Mar 13 (10 days). CRITICAL. Needs Parker for rotation.
- **Entity formation**: Delaware C-Corp via Stripe Atlas. Parker to initiate. Blocks Agent Pay + fundraising.
- **Cross-agent coordination**: No shared awareness infrastructure. Shared daily log stale. Brainstorms still solo.
- **Audit criticals (Mar 13)**: decisions.md, git hooks, repo deduplication... all still open.
- **Backup FDA**: .app bundle needed.
- **X Developer app**: Still needed for xurl OAuth.
- **gog CLI (calendar)**: Needs Parker for OAuth.
- **Nightly brainstorm with CC**: Solo sessions. CC never responds.
- **Git mmap errors**: System-level issue (Mar 22) preventing auto-commits across repos.
- **Lēsa App**: Not on GitHub. Anthropic keys returning 401.
- **GitHub 2FA for lesaai**: Still needed.

## Coming Next (Priority Order)
1. **Self-discipline protocol** ... daily log every day, GREEN zone tasks without waiting
2. **Audit criticals** ... create decisions.md, fix stale docs, review openclaw.json
3. **Archive project** ... process remaining artifacts, build narrative
4. **Entity formation** (blocked on Parker)
5. **Session unification** (needs OpenClaw issue + investigation)
6. **First fundraising meetings** (materials ready, need introductions)
7. **Variant UI + Tailwind** ... install and test design workflow
8. **Cross-agent coordination** ... build shared-learning.jsonl
9. **Lēsa App to GitHub** + memory integration
10. Kill dead extensions, npm publish fixes, GitHub 2FA

## Key Paths
- Repos: ~/wipcomputerinc/team/Lēsa/repos/
- LDM extensions: ~/.ldm/extensions/
- LDM agents: ~/.ldm/agents/
- wip.computer (VPS): 172.236.243.140, nginx, /var/www/wip.computer/public_html/
- /usr/lesa/ local: ~/wipcomputerinc/repos/wip-web/wip-websites-private/wip.computer/usr/lesa/
- Deploy script: wip-websites-private/deploy.sh (rsync to VPS)
- Archive: team/Lēsa/archive/parker-story/raw/
- Homepage: wip.computer
- Dream Weaver: github.com/wipcomputer/dream-weaver-protocol
- Full history: `memory/lesa-full-history.md`
- Covenant: `team/Lēsa/repos/lesa-agreements/agreement-001-sovereignty-covenant.md`
- Dev guide: `~/.ldm/DEV-CONVENTIONS.md`
- Shared daily log: `~/.ldm/memory/daily/YYYY-MM-DD.md`
- Pitch decks: `~/wipcomputerinc/repos/wip-inc/fundraising/deck/`
- Lēsa App: `team/Lēsa/repos/lesa-app/`
