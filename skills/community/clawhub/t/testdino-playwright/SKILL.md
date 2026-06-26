---
name: testdino-openclaw
description: Connect OpenClaw to TestDino for real-time Playwright CI intelligence. Ask about test failures, flaky tests, run history, and CI health in plain English.
homepage: https://github.com/testdino-hq/TestDino-OpenClaw-skills
metadata: {"openclaw": {"os": ["linux", "darwin", "win32"], "primaryEnv": "TESTDINO_PAT", "requires": {"bins": ["mcporter", "testdino-mcp"], "env": ["TESTDINO_PAT"]}, "install": [{"id": "npm-mcporter", "kind": "npm", "package": "mcporter", "bins": ["mcporter"], "label": "Install mcporter"}, {"id": "npm-testdino-mcp", "kind": "npm", "package": "testdino-mcp", "bins": ["testdino-mcp"], "label": "Install TestDino MCP"}]}}
---

# TestDino — Playwright CI Intelligence

Use the `exec` tool to call TestDino. Always use `mcporter`:

```
mcporter call testdino.<tool> [params]
```

**Important:** Always call `health` first to get the `projectId` unless the user has already provided it. Every other tool requires it.

---

## Commands (copy these exactly)

**Check connection / health check:**
```
exec: mcporter call testdino.health
```

**Project summary / CI overview / "summarize project X":**
```
exec: mcporter call testdino.health
exec: mcporter call testdino.list_testruns projectId=X by_time_interval=1d limit=5
```
Use the returned run IDs to fetch details if the user wants more depth.

**Show failures / failed tests (any time range):**

Resolve `TIME` from the user's words using the time mapping below, then run:
```
exec: mcporter call testdino.health
exec: mcporter call testdino.list_testcase projectId=X by_status=failed by_time_interval=TIME limit=10
```
The response includes `totalCount` — always use that as the total failure count.

**Show failures on a branch / any failures on branch Y? / new failures on branch Y?:**
```
exec: mcporter call testdino.health
exec: mcporter call testdino.list_testcase projectId=X by_branch=BRANCH_NAME by_status=failed limit=10
```

**CI summary / how did CI look / test run stats (any time range):**
```
exec: mcporter call testdino.health
exec: mcporter call testdino.list_testruns projectId=X by_time_interval=TIME
```

**Show recent test runs:**
```
exec: mcporter call testdino.health
exec: mcporter call testdino.list_testruns projectId=X limit=10
```

⚠️ **How to read list_testruns response:**
- The `testRuns` array is the complete flat list — use it directly, ordered newest first
- Each run has a `counter` field — always use this as the run number (e.g. "Run #10")
- Show ALL runs from `testRuns`, never skip any
- `rerunMetadata.isRerun: true` means this run is a retry — note it as "🔁 Retry of #[parentCounter]"

**Why did test run [ID or counter] fail? / Details for a specific test run:**

If the user provides a test run ID (e.g. `test_run_69c3d36648201d8fe8393e33`):
```
exec: mcporter call testdino.health
exec: mcporter call testdino.get_run_details projectId=X testrun_id=test_run_XXX
exec: mcporter call testdino.list_testcase projectId=X by_testrun_id=test_run_XXX by_status=failed limit=10
```

If the user provides a counter number (e.g. run #42):
```
exec: mcporter call testdino.health
exec: mcporter call testdino.get_run_details projectId=X counter=N
exec: mcporter call testdino.list_testcase projectId=X counter=N by_status=failed limit=10
```

**Why is [test name] failing? / Debug [test]:**

If the user did not provide a test name, ask: "Which test case name would you like to debug?" and wait for their answer before running anything.

Once you have the real test name, ALWAYS run these commands — even if a previous attempt failed. Never give generic advice instead of running the tool:
```
exec: mcporter call testdino.health
exec: mcporter call testdino.debug_testcase projectId=X testcase_name=EXACT TEST NAME WITHOUT QUOTES
```

**Show flaky tests / is [test] flaky? / is [test] flaky or a real bug?:**

If user names a specific test → use `debug_testcase` (it returns flakiness patterns).
If user asks generally → use:
```
exec: mcporter call testdino.health
exec: mcporter call testdino.list_testcase projectId=X by_status=flaky by_time_interval=TIME limit=10
```

**Is it safe to merge branch Y?:**

If no branch name was given, ask: "Which branch should I check?" and wait before running.
```
exec: mcporter call testdino.health
exec: mcporter call testdino.list_testcase projectId=X by_branch=Y by_status=failed limit=10
```

**Show timeout failures:**
```
exec: mcporter call testdino.health
exec: mcporter call testdino.list_testcase projectId=X by_error_category=timeout_issues by_time_interval=TIME limit=10
```

**List manual test cases / total count / show [priority] test cases / show [type] test cases:**

⚠️ Use `list_manual_test_cases` — NOT `list_testcase`. These are completely different tools.

```
exec: mcporter call testdino.health
exec: mcporter call testdino.list_manual_test_cases projectId=X limit=1000
```

⚠️ **IMPORTANT — verify the count:** After the response comes back, check the `count` field. If `count` is exactly 10, the API used its default limit and you do NOT have all results. You MUST retry with `limit=1000`:
```
exec: mcporter call testdino.list_manual_test_cases projectId=X limit=1000
```
Only trust the `count` from a response where you explicitly passed `limit=1000`.

Add filters if user specifies:
- `priority=critical` / `priority=high` / `priority=medium` / `priority=low`
- `type=smoke` / `type=regression` / `type=functional`
- `status=active` / `status=draft`

Examples:
- "critical priority test cases" → `list_manual_test_cases projectId=X priority=critical limit=1000`
- "smoke test cases" → `list_manual_test_cases projectId=X type=smoke limit=1000`

**If user asks for total count:** Read the `count` field from the response and reply with just the number.
**If user asks to list/show:** Show only caseId + title. Show the first 15, then ALWAYS end with:
_"There are more test cases available. Let me know if you'd like to see more!"_

**List test suites / show all suites:**
```
exec: mcporter call testdino.health
exec: mcporter call testdino.list_manual_test_suites projectId=X
```

Show only the `name` field from each suite. Show the first 15 suites, then end with:
_"There are more suites available. Let me know if you'd like to see more!"_

NEVER show: suite IDs, metadata, hierarchy, timestamps, descriptions (they are empty), or tags (they don't exist in the response). NEVER invent test case counts or test case names — `list_manual_test_suites` does NOT return test cases.

**List spec files / show spec files / all spec files in project:**
```
exec: mcporter call testdino.health
exec: mcporter call testdino.list_testruns projectId=X limit=1
exec: mcporter call testdino.get_run_details projectId=X counter=N
```
From the `get_run_details` response, extract `testSuites[].fileName` and list only the unique spec file names.

---

## Missing parameters

- No projectId → run health first to get it, unless user already provided it
- No test name → ask: "Which test case name?"
- No time range → ask: "Today (1d), 3 days (3d), 7 days, or monthly?"
- Test run ID vs counter → `testrun_id` accepts the full string ID; `counter` accepts a sequential number (e.g. `42`)

### Time range mapping (apply strictly before every query)

| User says | TIME value |
|---|---|
| today / right now / no time mentioned | `1d` |
| yesterday / last day | `1d` |
| last 2 days / 2 days | `3d` |
| last 3 days / 3 days | `3d` |
| last 5 days / 5 days | `3d` |
| this week / last week / 7 days / last 7 days / weekly | compute 7-days-ago and today as `YYYY-MM-DD,YYYY-MM-DD` e.g. `2026-03-23,2026-03-30` — do NOT use the `weekly` keyword (it has an exclusive boundary that drops the oldest day) |
| last 2 weeks / 14 days | `monthly` |
| this month / last month / 30 days / monthly | `monthly` |
| specific date e.g. "27 march 2026" / "27-03-2026" / "2026-03-27" | `2026-03-27,2026-03-28` (next day as end date) |
| date range e.g. "20 march to 25 march" | `2026-03-20,2026-03-25` |

Always normalize any date format the user gives to `YYYY-MM-DD`. For a specific single day, use `YYYY-MM-DD,YYYY-MM-DD+1` (end date = next day). For "last N days" not in the table, use `3d` if under 7 days, a computed date range (`YYYY-MM-DD,YYYY-MM-DD`) if exactly 7 days, `monthly` if over 7.

---

## Response format

**CRITICAL: NEVER invent or fabricate data.** Only show fields that exist in the actual API response. If a field is missing or empty, do not guess or fill it in. If the response is too large to process fully, show what you can and say "there are more — ask if you'd like to see more." Never make up descriptions, tags, test counts, or test case names that are not in the response.

**Keep responses short. Always use `totalCount` from the response for the count.**

**For list_testruns — use this exact format:**
```
**[ProjectName]** — [N] runs

- Run #[counter] — [Mon DD] | [branch] | ✅ [passed] passed ❌ [failed] failed[ | 🔁 Retry of #[parentCounter]]
- Run #[counter] — ...
```
NEVER include: run IDs, start times, durations, environment, author, status, total tests, skipped/flaky/timedOut counts.

**For list_testcase (failures) — use this exact format:**
```
**[ProjectName]** — **[totalCount] failures**

**Run #[counter]**
1. [test title]
2. [test title]

_(showing N of totalCount — ask for more if needed)_
```
ONLY show run number and test title. NEVER show test case IDs, run IDs, durations, status, start times, spec file paths.

- Merge safety: lead with yes/no then failure count
- Debug: 2-3 sentences on dominant pattern, note if flaky
- Show full details only if the user specifically asks
