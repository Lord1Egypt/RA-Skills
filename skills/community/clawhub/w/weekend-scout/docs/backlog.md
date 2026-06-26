# Weekend Scout -- Backlog

## Status legend
- `TODO` -- not started
- `IN PROGRESS` -- currently being worked on
- `DONE (YYYY-MM-DD)` -- completed
- `BLOCKED` -- waiting on something
- `DEFERRED` -- moved out of MVP scope

---

## Phase 1: Project Skeleton + Config

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1.1 | Create project structure (pyproject.toml, dirs, __init__ files) | DONE (2026-03-26) | |
| 1.2 | Implement config.py: default config generation | DONE (2026-03-26) | |
| 1.3 | Implement config.py: setup wizard (interactive prompts) | DONE (2026-03-26) | |
| 1.4 | Implement config.py: read/write YAML config | DONE (2026-03-26) | |
| 1.5 | Implement config.py: config path resolution (cross-platform) | DONE (2026-03-26) | |
| 1.6 | Implement __main__.py: CLI entry point with argparse subcommands | DONE (2026-03-26) | Done during scaffolding |
| 1.7 | Write tests for config.py | DONE (2026-03-26) | |
| 1.8 | Fix get_config_dir() for global pip installs (use ~/.weekend_scout when pyproject.toml absent) | DONE (2026-04-07) | pyproject.toml sentinel heuristic; new test for global-install path |

## Phase 2: City List + Distance

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2.1 | Add `download-data` CLI command: fetch + unzip cities15000.zip from GeoNames | DONE (2026-03-26) | |
| 2.2 | Implement cities.py: parse GeoNames file | DONE (2026-03-26) | |
| 2.3 | Implement distance.py: Haversine formula | DONE (2026-03-26) | Done during scaffolding |
| 2.4 | Implement distance.py: driving time heuristic | DONE (2026-03-26) | Done during scaffolding |
| 2.5 | Implement cities.py: filter by radius + assign tiers | DONE (2026-03-26) | |
| 2.6 | Implement cities.py: generate search queries (broad + targeted) | DONE (2026-03-27) | Redesigned to return templates+vars; `--city` override now geocodes coordinates/language |
| 2.7 | Create data/regions.json for Poland | DONE (2026-03-26) | Done during scaffolding |
| 2.8 | Implement cities.py: city list caching (JSON file) | DONE (2026-03-26) | |
| 2.9 | Wire "init" CLI command (returns config + cities + queries) | DONE (2026-03-26) | Wired during scaffolding; fully functional after Phase 3 |
| 2.10 | Write tests for cities.py and distance.py | DONE (2026-03-26) | |

## Phase 3: Event Cache

| # | Task | Status | Notes |
|---|------|--------|-------|
| 3.1 | Implement cache.py: SQLite schema creation | DONE (2026-03-26) | |
| 3.2 | Implement cache.py: save events (with dedup) | DONE (2026-03-26) | |
| 3.3 | Implement cache.py: query events by date range | DONE (2026-03-26) | |
| 3.4 | Implement cache.py: log searches | DONE (2026-03-26) | |
| 3.5 | Implement cache.py: mark events as served | DONE (2026-03-26) | |
| 3.6 | Implement cache.py: cleanup old events (30+ days) | DONE (2026-03-26) | |
| 3.7 | Wire cache CLI commands (save, cache-query, log-search, cache-mark-served) | DONE (2026-03-26) | Wired during scaffolding |
| 3.8 | Write tests for cache.py | DONE (2026-03-26) | |

## Phase 4: Telegram Sender

| # | Task | Status | Notes |
|---|------|--------|-------|
| 4.1 | Implement telegram.py: format message (Markdown) | DONE (2026-03-26) | |
| 4.2 | Implement telegram.py: send via Bot API (requests) | DONE (2026-03-26) | |
| 4.3 | Implement telegram.py: message splitting (>4096 chars) | DONE (2026-03-26) | |
| 4.4 | Wire "send" CLI command | DONE (2026-03-26) | Wired during scaffolding |
| 4.5 | Write tests for telegram.py (mock HTTP) | DONE (2026-03-26) | |

## Phase 5: Claude Code Skill

| # | Task | Status | Notes |
|---|------|--------|-------|
| 5.1 | Write SKILL.md with full search strategy prompt | DONE (2026-03-27) | Implemented in .claude/skills/weekend-scout/SKILL.md (177 lines, 6 steps) |
| 5.2 | Test /weekend-scout with real web searches | IN PROGRESS | Clean-run test done 2026-03-27: Phase A completed (4 searches, 0 events), interrupted before Phase B; exposed bugs fixed in 5.6 |
| 5.3 | Iterate on search queries based on result quality | DONE (2026-03-28) | Phase C rewritten: individual per-city searches, tier1→tier2→tier3 priority, budget allocation table; Phase D cap 3→5 fetches |
| 5.4 | Iterate on scoring rubric | TODO | |
| 5.5 | End-to-end test: init -> search -> save -> send | DONE (2026-04-04) | End-to-end scout flow validated in current skill runtime; Codex-specific validation is tracked separately in 12.17 |
| 5.6 | Budget config keys + low-results hint | DONE (2026-03-28) | max_searches(15)/max_fetches(15) in config.py + init JSON output; --low-results flag in format-message; console + Telegram hint when <3 results |
| 5.7 | Increase road trip options to 10 | DONE (2026-03-28) | max_trip_options=10 default, format_scout_message cap updated, Step 3/4 in skill template updated |

## Phase 6: Polish

| # | Task | Status | Notes |
|---|------|--------|-------|
| 6.1 | Add region mappings beyond Mazowsze | DONE (2026-03-27) | data/regions.json expanded to ~80 EU cities (Berlin, Paris, Vienna, Budapest, Brussels, etc.) |
| 6.2 | Handle "no events found" gracefully | DONE (2026-03-27) | format_scout_message returns "No events found" message when both city_events and trip_options are empty |
| 6.3 | Add cron/scheduled execution instructions to README | TODO | |
| 6.4 | Cross-platform testing (Windows native, WSL) | TODO | Broader matrix still pending; Claude Code and Codex skill flows are already end-to-end tested |

## Phase 7: Post-Launch Tuning

| # | Task | Status | Notes |
|---|------|--------|-------|
| 7.1 | Switch Telegram formatting to native HTML | DONE (2026-03-27) | parse_mode="HTML"; html.escape() for all user text; bold/italic/links via <b>/<i>/<a> |
| 7.2 | Unified JSONL action logging | DONE (2026-03-27) | log_action() in cache.py + log-action CLI; all phases/lifecycle events logged to action_log.jsonl with run_id |
| 7.3 | Cache-only mode for skill (--cached-only) | DONE (2026-03-27) | SKILL.md skips Step 2 when flag set |
| 7.4 | Pin skill to Haiku model | DONE (2026-03-27) | model: haiku frontmatter in SKILL.md |
| 7.5 | Inline [link] on description/venue line | DONE (2026-03-27) | Removed separate source footer; link appended to desc line (or venue if no desc); trip url field added |
| 7.6 | Fix "Leave by:" departure timing rule | DONE (2026-03-27) | Formula: event_start + 1h30 − drive_time, min 09:00; documented in SKILL.md Step 4 |
| 7.7 | Logging enhancements (events_discovered, skip actions, run_complete) | DONE (2026-03-27) | --events-discovered on log-search; --run-id on save; skip vs phase_start logic; run_complete in Step 6 |
| 7.8 | Expand language/country support to 27 countries | DONE (2026-03-27) | Added IT/ES/PT/NL/SE/NO/DK/FI/RO/HR/BG/RS/GR/TR/RU with month names and query templates |
| 7.9 | Fix first-run onboarding: needs_setup guard in init + SKILL.md gate | DONE (2026-03-27) | init returns needs_setup:true when home_city blank; SKILL.md shows setup msg and stops |
| 7.10 | Fix --events-discovered CLI type error (int vs list) | DONE (2026-03-27) | SKILL.md log pattern clarified: integer count, not a list |
| 7.11 | Refresh Telegram digest visual styling + preview parity | DONE (2026-04-06) | Follow-up styling pass completed: `🗓` header, `🏙` home-city icon, no summary line, compact trip route summaries, and robust `free_entry` handling for bool/string values |

| 7.12 | Expand supported countries for high-adoption markets | DONE (2026-04-15) | Added US/CA/GB/IE/AU/NZ/SG/JP/KR, country-aware city lookup hints for init/setup, and dedicated `ja`/`ko` query/date support |

## Phase 8: Onboarding & UX

| # | Task | Status | Notes |
|---|------|--------|-------|
| 8.1 | Redesign setup wizard: city-only input, auto-geocode from GeoNames | DONE (2026-03-27) | run_setup_wizard asks only city + radius; auto-fills coords/country/lang; multi-country disambiguation; testable via _geonames_path param |
| 8.2 | Add find-city CLI command | DONE (2026-03-27) | python -m weekend_scout find-city --name X [--country Y]; returns JSON matches from GeoNames; no-file warning |
| 8.3 | Add setup --json flag for skill-driven config | DONE (2026-03-27) | python -m weekend_scout setup --json '{...}'; merges into config, invalidates stale city cache |
| 8.4 | Fix DEFAULT_CONFIG: remove hardcoded Poland/Warsaw defaults | DONE (2026-03-27) | home_country:"", home_coordinates:{lat:0.0,lon:0.0}; 0,0 is the unset sentinel |
| 8.5 | SKILL.md: full in-chat onboarding flow (find-city + WebSearch fallback + setup --json) | DONE (2026-03-27) | Handles needs_setup + coordinates_not_set; no manual terminal setup needed |
| 8.6 | SKILL.md: always display message to user; improved Telegram unconfigured guidance | DONE (2026-03-27) | Message shown in chat; config commands suggested when Telegram not set |

## Phase 9: Multi-Platform Restructuring

| # | Task | Status | Notes |
|---|------|--------|-------|
| 9.1  | Create weekend_scout/regions.py from data/regions.json | DONE (2026-03-28) | ~200 entries, all 27 countries, English + native names |
| 9.2  | Update cities.py to import from regions.py | DONE (2026-03-28) | get_region_name() now does case-insensitive lookup via REGIONS dict |
| 9.3  | Move GeoNames download target to platformdirs cache dir | DONE (2026-03-28) | _geonames_dir() uses get_config_dir()/geonames/ |
| 9.4  | Add auto-download in init/find-city when file missing | DONE (2026-03-28) | ensure_geonames() helper; called from get_city_list, cmd_find_city, cmd_init, run_setup_wizard |
| 9.5  | Update tests for new data paths | DONE (2026-03-28) | Monkeypatch _geonames_dir; added test_regions.py; 144 tests pass |
| 9.6  | Delete data/ directory from repo | DONE (2026-03-28) | git rm data/regions.json; data/ removed |
| 9.7  | Create skill_template/ with generator system | DONE (2026-03-28) | platforms.yaml, weekend-scout.template.md, generate.py, README.md |
| 9.8  | Create docs/platform-skill-reference.md | DONE (2026-03-28) | Copied from platform-skill-research.md |
| 9.9  | Generate .claude/skills/weekend-scout/SKILL.md from template | DONE (2026-03-28) | Replaced existing file |
| 9.10 | Create .codex/skills/weekend-scout/ with generated SKILL.md | DONE (2026-03-28) | Plus agents/openai.yaml |
| 9.11 | Create .openclaw/skills/weekend-scout/ with generated SKILL.md | DONE (2026-03-28) | |
| 9.12 | Create install/install_skill.py | DONE (2026-03-28) | Cross-platform installer with auto-detect |
| 9.13 | Create install/README.md | DONE (2026-03-28) | Per-platform install instructions |
| 9.14 | Rewrite root README.md for multi-platform | DONE (2026-03-28) | |
| 9.15 | Update CLAUDE.md with new paths and workflow | DONE (2026-03-28) | |
| 9.16 | Update .gitignore | DONE (2026-03-28) | Removed data/cities15000.txt; added note about generated skills |
| 9.17 | Update docs/design_changes.md | DONE (2026-03-28) | Logged all Phase 9 structural changes |
| 9.18 | Final test run + commit | DONE (2026-03-28) | 144 tests pass; generate --check passes |

## Phase 10: Installation Fixes

| # | Task | Status | Notes |
|---|------|--------|-------|
| 10.1 | Bundle SKILL.md files as package data | DONE (2026-03-28) | `weekend_scout/skill_data/` + pyproject.toml package-data; generator mirrors there |
| 10.2 | Add install-skill CLI command | DONE (2026-03-28) | Copies SKILL.md from package to global skills dir; auto-detects platform |
| 10.3 | Fix install/install_skill.py: use pip install (not -e) | DONE (2026-03-28) | `--dev` flag for editable; delegates skill copy to `install-skill` CLI |
| 10.4 | Update README with user vs developer flows | DONE (2026-03-28) | |
| 10.5 | Update CLAUDE.md | DONE (2026-03-28) | |
| 10.6 | Update docs/design_changes.md | DONE (2026-03-28) | |
| 10.7 | Test both install flows | DONE (2026-03-28) | Smoke-tested via manual CLI commands |
| 10.8 | Improve pip-missing + PEP 668 error guidance on Linux | DONE (2026-04-07) | Detect PEP 668 in ensurepip failures; show two-step guidance (install pip via package manager + rerun with --break-system-packages) |

## Phase 11: Skill Workflow Drift Fixes

| # | Task | Status | Notes |
|---|------|--------|-------|
| 11.1 | Move generated Codex repo skill from `.codex/skills/` to `.agents/skills/` | DONE (2026-03-29) | Keeps repo artifact aligned with current Codex discovery docs |
| 11.2 | Keep `.openclaw/skills/` as generated repo artifact but document it as packaging/staging only | DONE (2026-03-29) | Supported installed OpenClaw location remains `~/.openclaw/skills/` |
| 11.3 | Fix OpenClaw generated metadata format and remove unsupported pip installer metadata | DONE (2026-03-29) | `metadata` now single-line JSON; removed `kind: "pip"` block |
| 11.4 | Update installers, docs, and tests for the new Codex install target | DONE (2026-03-29) | Codex now installs to `~/.agents/skills/` |
| 11.5 | Create python symlink (python3 → python) on POSIX if needed | DONE (2026-04-10) | `_ensure_python_symlink()` creates `~/.local/bin/python` pointing to `python3` when only `python3` exists in PATH; runs after pip install succeeds |
| 11.6 | OpenClaw direct delivery when Telegram not configured | DONE (2026-04-10) | Platform-conditional delivery-and-audit reference: OpenClaw reads the formatted message file and outputs directly to chat; non-OpenClaw platforms show Telegram config instructions |
| 11.7 | OpenClaw installer: suppress codex when openclaw detected | DONE (2026-04-10) | `detect_platforms()` removes codex from detected list when openclaw is present, because OpenClaw creates `~/.agents` for Plugin Bundle discovery — prevents false-positive Codex detection |

## Phase 12: Skill Reliability Refactor

| # | Task | Status | Notes |
|---|------|--------|-------|
| 12.1 | Add `audit-run` CLI validation for logged scout runs | DONE (2026-04-03) | Validates phase sequencing, phase completion, post-D discovery, accounting, and run_complete consistency |
| 12.2 | Extend `init-skill` with explicit workflow task cards | DONE (2026-04-03) | Compact `init-skill` now keeps broad queries and tier1 cards only; later tiers are requested on demand in small batches |
| 12.3 | Refactor generated runtime skill into orchestrator + bundled references | DONE (2026-04-03) | Core SKILL.md now points to `onboarding`, `search-workflow`, `scoring-and-trips`, and `delivery-and-audit` references instead of inlining the full protocol |
| 12.4 | Extend generator/package data to mirror bundled skill resources | DONE (2026-04-03) | `skill_template/resources/` now mirrors into repo skills and `weekend_scout/skill_data/` |
| 12.5 | Add regression coverage for workflow auditing and split references | DONE (2026-04-03) | Added fixture-based audit regression coverage and tests for bundled reference mirroring |
| 12.6 | Add deterministic helper commands for phase/score/run summaries | DONE (2026-04-03) | Added `phase-summary`, `score-summary`, and `run-complete` so the skill no longer hand-builds summary payloads |
| 12.7 | Add on-demand `phase-c-cities` batching for later targeted-search tiers | DONE (2026-04-03) | Tier2/tier3 now come back in explicit small batches filtered against covered cities and already-done searches |
| 12.8 | Make audit advisory in normal runtime flow | DONE (2026-04-03) | `audit-run` is non-blocking by default and only fails the command in `--strict` mode |
| 12.9 | Align `init` and `init-skill` around one compact runtime contract | DONE (2026-04-03) | `init` now mirrors `init-skill` at the top level and moves full debug-only material under `debug` |
| 12.10 | Shrink `workflow` to dynamic run data only | DONE (2026-04-03) | Removed static policy from runtime `workflow`; references now own phase order and logging rules |
| 12.11 | Add safe transport-artifact cleanup in cache dir | DONE (2026-04-03) | `init`/`init-skill` clean known transport files at startup, and `run-complete` cleans them again after success |
| 12.12 | Log later-tier batch requests in action_log | DONE (2026-04-03) | `phase_c_batch_requested` now records tier, offset, limit, coverage, eligibility, and returned counts |
| 12.13 | Trim remaining init workflow card noise | DONE (2026-04-03) | Removed unused `minimum_trip_cities` / per-card metadata, renamed `already_done` to `query_already_done`, and kept full later-tier cards only in `init.debug` |
| 12.14 | Restore monolith-grade split skill guardrails | DONE (2026-04-04) | Re-expanded split Step 2 lifecycle commands from `main`, refactored command-failure handling into a global contract rule, and added authoritative example-command validation coverage |
| 12.15 | Make later-tier targeting deterministic and split validation fetch reserve | DONE (2026-04-04) | Removed tier2/tier3 heuristic gates, made `phase-c-cities` a pure batch helper, and split Phase D validation fetch accounting from the main discovery fetch budget |
| 12.16 | Persist run-scoped candidates during discovery and save from session | DONE (2026-04-04) | Added JSON run-session candidate store, `session-query`, `save --from-session`, `log-search --events(-file)`, and internal coverage/uncovered-tier1 derivation |
| 12.17 | Validate Codex skill end-to-end | DONE (2026-04-04) | Codex full scout workflow is now end-to-end tested alongside Claude Code |
| 12.18 | Stabilize candidate canonicalization, rerun tier1 retries, and digest prep | DONE (2026-04-05) | Added country enrichment, conservative alias merge, exact-key DB field upgrades, rerun-aware tier1 cards, and `prepare-digest` for grouped scoring input |
| 12.19 | Tighten session dedup identity and align served/docs contract | DONE (2026-04-05) | Removed URL-only session merges, made `cache-mark-served` use weekend-overlap semantics, and aligned runtime docs/skill wording with the shipped `init-skill` contract |
| 12.20 | Make served logging run-scoped and restore broad fallback country | DONE (2026-04-05) | `cache-mark-served` now requires `--run-id` so successful sends satisfy `audit-run`; the English fallback broad query again appends `{country}` |
| 12.21 | Ignore accidental repo-root temp folders and remove leftovers | DONE (2026-04-05) | Added root ignore rules for `ws_audit_*` and `tmp*` scratch dirs, and removed the current leftovers from the repo root |
| 12.22 | Harden phase lifecycle on reruns and simplify phase entry flow | DONE (2026-04-06) | Auto-open missing phase starts in runtime logging, tighten audit lifecycle checks, and rewrite search-workflow phase sections to start before skip/work branching |
| 12.23 | Add centralized Python failure logging and structured CLI errors | DONE (2026-04-06) | Introduced `python_failures.jsonl`, a shared command failure wrapper, authoritative structured Telegram send results, and skill-facing `error`/`failure_id` reporting |
| 12.24 | Add Codex-only one-shot elevated resend for Telegram network blocks | DONE (2026-04-06) | The Codex skill now requests one approval-gated resend only for `send_failed` + `telegram_network_blocked`, and audit coverage locks final delivery state to the last `telegram_send` entry |
| 12.25 | Make `--cached-only` rejoin the normal end-to-end flow | DONE (2026-04-06) | Clarified cached-only as a discovery bypass that logs `skip --phase search`, builds `digest_input` from cache, and then continues through normal scoring, Telegram send, and audit |
| 12.26 | Preserve event URLs from skill payloads into session/cache | DONE (2026-04-06) | Common references now keep `source_url` in event/trip payloads when known, and `log_search()` backfills missing event URLs from fetch queries |
| 12.27 | Bind installed skills to the installing Python interpreter | DONE (2026-04-07) | Installed skill files now rewrite runtime commands to the installing interpreter, pip-backed installs preserve the resolved target platforms, the copy-only repo installer preflights an existing runtime, the bootstrap installer imports repo-local helpers correctly before pip install in a fresh clone, `--with-pip` auto-attempts stdlib `ensurepip` when `pip` is missing, failed `ensurepip` recovery prints OS-aware manual guidance, PEP 668 failures support an explicit `--break-system-packages` override plus scoped retry guidance, post-install package commands run from a neutral cwd instead of the repo checkout, and `--uninstall` now removes global skill files plus the `weekend-scout` package while preserving `.weekend_scout` runtime data |
| 12.28 | Normalize OpenClaw internal delivery status and audit handling | DONE (2026-04-14) | Kept one shared delivery reference, made OpenClaw delivery-channel wording explicit, and mapped final OpenClaw `run_complete.send_reason` to `telegram_internal` while preserving raw `send` output |
| 12.29 | Embed delivery stats and staged audit notes into the actual formatted message | DONE (2026-04-14) | Added `prepare-delivery`, staged `audit-run`, formatter support for stats/notes blocks, delivery-reference updates across platforms, regenerated skill assets, and regression coverage |

## Phase 13: Workflow Modes

| # | Task | Status | Notes |
|---|------|--------|-------|
| 13.1 | Add --research-only skill argument for mid-week cache-building runs | DONE (2026-04-10) | Stops before Step 5; full discovery + scoring, no format/send; scheduling pattern documented in README |
| 13.2 | Remove retired MVP design doc and normalize docs history ordering | DONE (2026-04-17) | Deleted the retired MVP design doc, cleaned surviving references, and reordered `docs/design_changes.md` newest-first |
| 13.3 | Fix Windows bash backslash-mangling of cache_dir paths | DONE (2026-04-17) | `init`/`init-skill` now emit `cache_dir` as forward-slash POSIX form, `_load_json_argument` rejects drive-letter paths with no separator, and platform-transport reference tells the skill to use `cache_dir` verbatim |
| 13.4 | Add repo-root SKILL.md for Skills Directory routing | DONE (2026-04-22) | Root file stays platform-neutral, explains the multi-platform layout, and routes readers to the generated runtime skill for their platform |
| 13.5 | Turn repo-root SKILL.md into a permanent bundle bootstrap dispatcher | DONE (2026-04-22) | Root skill now bootstraps the bundle runtime in place, dispatches to nested platform skills, and uses `install/install_skill.py --runtime-only` to avoid shared/global skill-copy side effects for workspace-installed bundles |
