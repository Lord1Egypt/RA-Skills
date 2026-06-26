---
name: x-bookmarks-digest
description: Automatically review X/Twitter bookmarks for useful tools, projects, repos, products, and ideas. Fetches via xurl, analyses for value, and outputs an actionable digest with proposed next steps — including clawhub installs or new skill scaffolding.
version: 1.0.0
author: openclaw
triggers:
  - "digest x bookmarks"
  - "check my bookmarks"
  - "x bookmarks"
  - "twitter bookmarks"
  - "bookmark digest"
  - "review bookmarks"
  - "bookmarks digest"
metadata:
  openclaw:
    emoji: "🔖"
    version: "1.0.0"
    author: "openclaw"
    requires:
      bins: ["python3", "xurl"]
---

# X Bookmarks Digest

Fetch, analyse, and digest your X/Twitter bookmarks into actionable insights.

## When to Use

Activate this skill when the user says anything like:
- "digest x bookmarks"
- "check my bookmarks"
- "review my x bookmarks"
- "what's interesting in my bookmarks?"
- "bookmark digest"
- "any good stuff in my twitter bookmarks?"

## Prerequisites Check

Before running the workflow, verify xurl authentication:

```bash
xurl whoami
```

**If 401/Unauthorized:**
Tell the user to set up xurl authentication:
```
xurl auth apps add <app-name> --client-id <id> --client-secret <secret>
```
Then run `xurl auth default <app-name>` to set it as default.
Do NOT proceed until auth works. Stop and report the issue.

## Workflow — Step by Step

### Step 1: Check Rate Limit

Read the state file to check when the last run was:

```bash
cat {baseDir}/state.json 2>/dev/null || echo '{"last_bookmark_id": null, "last_run_ts": null, "processed_count": 0}'
```

If `last_run_ts` is less than 1 hour ago, warn the user:
> "Last digest was run at {time}. Free tier allows max 1 run/hour. Use --force to override."

Only proceed if:
- No previous run exists, OR
- More than 1 hour has elapsed, OR
- User explicitly says to force/override

### Step 2: Fetch Bookmarks

Run the fetch script to get new bookmarks:

```bash
python3 {baseDir}/scripts/fetch_bookmarks.py --count 50
```

Options:
- `--count N` — number of bookmarks to fetch (default 50, max 100)
- `--force` — skip rate limit check
- `--all` — fetch all (ignore last-checked ID, reprocess everything)

**Output:** JSON array of bookmark objects to stdout.
**Side effect:** Updates `{baseDir}/state.json` with new watermark.

If the output is empty or `[]`, report: "No new bookmarks since last check."

### Step 3: Analyse Bookmarks

Pipe the fetched bookmarks through the analyser:

```bash
python3 {baseDir}/scripts/fetch_bookmarks.py --count 50 | python3 {baseDir}/scripts/analyse_bookmarks.py
```

Or if you saved fetch output to a variable, pass it via file:

```bash
python3 {baseDir}/scripts/analyse_bookmarks.py --file /tmp/bookmarks.json
```

**Output:** Structured JSON with categories and relevance scores:
```json
{
  "summary": {"total": 50, "new": 12, "high": 4, "medium": 5, "low": 3},
  "bookmarks": [
    {
      "id": "123",
      "text": "...",
      "author": "@user",
      "category": "tool",
      "relevance": 5,
      "urls": ["https://github.com/..."],
      "github_repos": ["user/repo"],
      "keywords": ["python", "cli"]
    }
  ]
}
```

### Step 4: Generate Digest

Using the structured analysis output, write a digest following this format:

```markdown
# X Bookmarks Digest — {date}

## Summary
- {total} bookmarks checked, {new} new since last run
- {high} high-value, {medium} medium, {low} low

## High Value (relevance 4-5)

### [{category}] {title or key topic}
@{author}: "{first 100 chars of text}..."
- URL: {extracted url}
- Why: {1-line explanation of value}
- Action: {specific next step}

## Medium Value (relevance 3)
{same format, briefer}

## Proposed Actions
1. [ ] {action 1}
2. [ ] {action 2}
...
```

### Step 5: Decide on Actions

For each high-value bookmark, decide:

| Bookmark Type | Action |
|--------------|--------|
| **GitHub repo / tool** | Propose `git clone` or `brew install` |
| **Clawhub-compatible skill** | Propose `clawhub install <slug>` |
| **Interesting project to build** | Propose scaffolding a new skill in `skills/` |
| **Useful article/thread** | Propose saving to Obsidian vault |
| **Tip/technique** | Propose saving to OpenClaw memory |

Ask the user which actions to execute. Do not auto-execute without confirmation.

### Step 6: Update State

After successful digest, verify state was updated:

```bash
cat {baseDir}/state.json
```

Should show updated `last_bookmark_id` and `last_run_ts`.

## Error Handling

| Problem | Action |
|---------|--------|
| **xurl not found** | Tell user: `brew install xurl` |
| **xurl 401** | Guide user through `xurl auth apps add` setup |
| **xurl 429 (rate limit)** | Report rate limit hit. Suggest waiting 15 mins. |
| **Empty bookmarks** | Report "No bookmarks found" — user may need to bookmark posts first |
| **No new bookmarks** | Report "No new bookmarks since {last_run_ts}" |
| **state.json missing** | First run — create fresh state after fetch |
| **Python error** | Print stderr, check Python 3.10+ installed |

## Test Commands

Quick test (dry run, no state update):
```bash
# Test xurl auth
xurl whoami

# Test fetch (small batch)
python3 {baseDir}/scripts/fetch_bookmarks.py --count 5 --force

# Test analyse (with sample data)
echo '[{"id":"1","text":"Check out this amazing CLI tool https://github.com/user/repo","author_username":"devuser","created_at":"2026-03-19T10:00:00Z"}]' | python3 {baseDir}/scripts/analyse_bookmarks.py

# Full pipeline test
python3 {baseDir}/scripts/fetch_bookmarks.py --count 10 --force | python3 {baseDir}/scripts/analyse_bookmarks.py
```

Or just say: **"digest x bookmarks"** to run the full workflow.

## Configuration

All config is in `{baseDir}/state.json`:
- `last_bookmark_id` — watermark for incremental fetches
- `last_run_ts` — rate limit enforcement
- `processed_count` — running total of processed bookmarks

No additional configuration files needed. xurl manages its own auth.
