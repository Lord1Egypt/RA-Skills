---
name: reviews-to-github-issues
description: Turns recent negative App Store / Google Play reviews into deduplicated GitHub issues - one issue per problem topic, with linked and quoted reviews, new reviews added as comments to the existing issue instead of duplicates. Uses AppGoat review data and the gh CLI (or the GitHub MCP server). Use when the user says "turn reviews into issues", "file bugs from app reviews", "what are users complaining about, make tickets", "sync App Store reviews to GitHub" or sets up a daily review triage.
argument-hint: "<app> <repo> [since]"
license: MIT
---

# Reviews → GitHub issues

Reads the app's recent 1–3★ reviews, groups them into problem topics (a crash, a confusing
paywall, a missing feature), and keeps exactly one GitHub issue per topic up to date. Running it
again never duplicates: issues carry a hidden marker, and reviews already linked are skipped.

It can also run on AppGoat events (`negative_review_spike`, `review_spike`, `rating_drop` from a
watch on the app) instead of a schedule; see **Automate it**.

## When to use

- The user wants app store feedback in their issue tracker, once or on a schedule.
- Not for answering reviews (use `reply-to-every-review` with a connected store account) or for a one-off
  sentiment summary (use `app-audit-lite`).

## Inputs

- `app` (required): store URL, Apple id, Play package, bundle id or name.
- `repo` (required): `owner/name` of the GitHub repository. Default: the current repo
  (`gh repo view --json nameWithOwner -q .nameWithOwner`).
- `since` (optional): ISO date; default 7 days ago. Overlapping windows are safe (dedupe by review id).

Limits per run unless the user says otherwise: country `us` (add others on request), at most
**5 new issues** per run, at most 3 review pages.

## Steps

Costs in AppGoat credits; GitHub calls are free. Without the MCP, use the REST equivalents in
[reference/api.md](reference/api.md).

1. `get_app` {app} - **1** (+1 if refreshed). Note store, app_id, title, current version.
2. Existing topics (free): `gh issue list --repo <repo> --label appgoat-reviews --state all --limit 200 --json number,title,state,body`.
   Read the `<!-- appgoat:topic=<slug> app=<store:id> -->` markers so you reuse existing slugs
   for the same problem instead of inventing new ones.
3. `get_reviews` {app, country: "us", rating: "1-3", since, limit: 100} - **1 per page** (+1 if the
   US reviews are refreshed). Follow `next_cursor` for up to 3 pages. Reviews carry AI tags
   (`sentiment`, `intent`, `severity` 0–3, `topic`) once tagged; untagged ones have them null.
   Use a tagged review's `topic` as the starting point for the slug and `severity` ≥ 2 as "high".
   Do not filter by `intent`/`topic` here: the filters drop untagged reviews, so read the
   whole 1–3★ window and classify the untagged ones yourself.
4. Group the reviews into topics (no calls). A topic is one concrete problem ("login loop after
   update", "widget doesn't refresh"), not a mood ("bad app"). Give each a lowercase slug
   (`login-loop`), reuse an existing slug when it is the same problem. Skip praise, spam, pure
   pricing rants with no actionable ask, and reviews under 20 characters.
5. For each topic, from most reviews to fewest:
   - `bash scripts/upsert_issue.sh find --repo <repo> --app <store:app_id> --topic <slug>` prints the
     issue (or `none`) and the review ids it already links. Drop those reviews.
   - Apply the decision rules, write the body to a temp file, then
     `bash scripts/upsert_issue.sh upsert --repo <repo> --app <store:app_id> --topic <slug> --title "<title>" --body-file <file> [--reopen]`.
   - With the **GitHub MCP server** instead of gh: `search_issues` with `repo:<repo> label:appgoat-reviews "appgoat:topic=<slug>" in:body`,
     then `add_issue_comment`, `update_issue` (state open) or `create_issue` with the marker as the
     first line of the body and the label `appgoat-reviews`.
6. Report what was created, commented and skipped.

Budget: **2–10 credits** per run (1 app lookup + 1–3 review pages + refreshes).

## Decision rules

- **New issue** when the topic has no issue yet and either ≥ 2 reviews in the window, or 1 review
  mentioning a crash, data loss, a payment/subscription charge problem, a login lockout or a
  security/privacy problem. Otherwise list it under "watching" in the run report, no issue.
- **Comment** on the open issue when it exists and there are new (not yet linked) reviews.
- **Closed issue:** reopen (`--reopen`) when a new review is for a version released after the issue
  was closed or names the same symptom within 30 days of closing; otherwise create a new issue
  (the script links the old one).
- **Never** paste reviewer names or any personal data into issues; quote at most 200 characters per
  review; do not edit or close issues; do not assign people.
- **Title:** `<Problem> (<n> reviews, <store>)`, ≤ 80 characters, e.g. `Login loop after 3.2 update (4 reviews, App Store)`.
- **Labels:** always `appgoat-reviews`; add `bug` for crashes/errors or `enhancement` for feature
  requests only if those labels already exist in the repo.
- **Severity line:** `high` = crash, data loss, payment, lockout; `medium` = a broken feature with a
  workaround; `low` = UX friction or a feature request.
- Stop after 5 new issues; mention the remaining topics in the report.

Review links: Play `https://play.google.com/store/apps/details?id=<package>&reviewId=<review_id>`;
Apple has no per-review URL, so use `https://apps.apple.com/<country>/app/id<app_id>?see-all=reviews`
and give the review id. Always write `review:<review_id>` on the review's line so later runs dedupe.

## Output format

New issue body (the script prepends the marker):

```markdown
**Severity:** high · **Store:** App Store (us) · **Versions:** 3.2.0, 3.2.1 · **First seen:** 2026-10-18

<2-3 sentences: what users experience, when it started, any pattern (device, OS, version).>

### Reviews
- ★1 · v3.2.1 · 2026-10-20 · "Since the update it logs me out every time I open it…" · [store](https://apps.apple.com/us/app/id284882215?see-all=reviews) · review:11223344
- ★2 · v3.2.0 · 2026-10-19 · "…" · [store](…) · review:11223399

### Suggested next step
<one concrete debugging or product step>

_From AppGoat review data. Updated automatically; new reports are added as comments._
```

Comment on an existing issue:

```markdown
**<n> new reviews** (<since> → <today>), versions <v>:
- ★1 · v3.2.1 · 2026-10-21 · "…" · [store](…) · review:11224000
```

Run report (to the user):

```markdown
Reviews → issues for <app> since <date>: <n> reviews read, <t> topics.
- Created #123 Login loop after 3.2 update (4 reviews)
- Commented #98 Widget not refreshing (+2)
- Watching: dark mode request (1), price complaint (1)
Credits used: <sum>.
```

## Automate it

Daily triage in the repository that should receive the issues.

GitHub Action (`.github/workflows/appgoat-reviews.yml`, secrets `ANTHROPIC_API_KEY`, `APPGOAT_API_KEY`):

```yaml
name: AppGoat reviews to issues
on:
  schedule:
    - cron: "0 6 * * *"
  workflow_dispatch:
permissions:
  contents: read
  issues: write
jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install AppGoat playbooks and MCP config
        env:
          APPGOAT_API_KEY: ${{ secrets.APPGOAT_API_KEY }}
        run: |
          git clone --depth 1 https://github.com/appgoat/skills /tmp/appgoat-skills
          mkdir -p .claude/skills
          cp -r /tmp/appgoat-skills/skills/* .claude/skills/
          # Hosted AppGoat MCP server; the key goes into a file, not the command line.
          jq -n --arg key "$APPGOAT_API_KEY" \
            '{mcpServers: {appgoat: {type: "http", url: "https://api.appgoat.ai/mcp", headers: {"x-api-key": $key}}}}' \
            > "$RUNNER_TEMP/appgoat-mcp.json"
      - uses: anthropics/claude-code-action@v1
        env:
          GH_TOKEN: ${{ github.token }}
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Use the reviews-to-github-issues skill for app <app link>, repo ${{ github.repository }}, since 2 days ago.
            The helper script is at .claude/skills/reviews-to-github-issues/scripts/upsert_issue.sh.
          claude_args: |
            --mcp-config ${{ runner.temp }}/appgoat-mcp.json
            --allowedTools mcp__appgoat__get_app,mcp__appgoat__get_reviews,mcp__appgoat__get_job,Write,Bash(gh issue list:*),Bash(gh label list:*),Bash(bash .claude/skills/reviews-to-github-issues/scripts/upsert_issue.sh:*)
```

On events instead of a schedule: a watch on the app plus either a `kind: github` webhook that
starts [events/appgoat-events.yml](events/appgoat-events.yml) through `repository_dispatch` (paid
plans), or a routine that polls `get_events` / `GET /v1/events` (free, every plan, state kept by
`scripts/poll_events.sh`). Setup, curl calls and routine prompts: [events/README.md](events/README.md).

Claude Code routine (with the AppGoat connector and GitHub access):

```text
/schedule weekdays 08:00 - Run the reviews-to-github-issues playbook for <app link> into <owner/repo>, since the previous run (default 3 days). Post the run report as a summary.
```
