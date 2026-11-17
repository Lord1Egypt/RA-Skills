---
name: reply-to-every-review
description: Drafts a reply to every unanswered App Store and Google Play review of the user's own app, in the app's voice, through their connected App Store Connect / Play Console account - each reply is a dry run with a before/after diff and AppGoat guardrail scores (policy, tone, claims), and only the replies the user approves are posted. Use when the user says "reply to my reviews", "answer every review", "respond to unanswered reviews", "draft review replies", "clear the review backlog" or sets up daily review replies.
argument-hint: "[app] [since]"
license: MIT
---

# Reply to every review

Finds the reviews of the user's app that have no developer reply, writes a short, specific reply
to each, and posts the ones the user approves. Nothing is posted without a dry run the user has
seen: every reply goes through `propose_action` (dry run, free) and then `apply_action`.

## When to use

- The user owns the app and has connected App Store Connect and/or Play Console in AppGoat
  (https://dash.appgoat.ai/connections).
- Not for competitors' apps (use `app-audit-lite`) or for filing bugs (use `reviews-to-github-issues`).

## Inputs

- `app` (optional): a linked app (App Store id or Play package). Default: every app linked to an
  `asc` or `play_console` connection; ask which one when there are more than three.
- `since` (optional): ISO date; default all unanswered reviews (Play only returns the last 7 days).

Ask the user once, before drafting, for anything you cannot infer: the app's voice (default:
friendly, plain, first person plural "we"), the support address to point to (default: the
support URL in the listing), and whether there is a known fix or release to mention.

Limits per run unless the user says otherwise: at most **30 replies**, lowest stars and newest first.

## Steps

Costs in AppGoat credits. Without the MCP, use the REST equivalents in [reference/api.md](reference/api.md).

1. `list_connections` {} - **0**. Keep `asc` and `play_console` connections with `status: active`
   and the app linked. `mode: read_only` can dry-run but not post: tell the user and continue
   with drafts only. No connection: send the user to https://dash.appgoat.ai/connections and stop.
2. For each connection and app: `read_connection` {id, what: "reviews", app, unanswered: true,
   limit: 100} - **1 per page**, follow `next_cursor` up to 3 pages. Each review has a
   `review_id`, rating, title, body, language, version and date. Drop reviews older than `since`.
3. Optional prioritising: `get_reviews` {app, rating: "1-3", intent: "bug,crash", limit: 100} -
   **1** returns AppGoat's AI tags (`intent`, `severity`, `topic`) for public reviews. Match by
   text and date; answer `bug`/`crash` reviews with severity ≥ 2 first and group same-topic
   reviews so their replies are consistent (not identical).
4. Draft one reply per review (no calls), following the decision rules. Reply in the review's language.
5. For each draft: `propose_action` {type: "review.reply", connection: <id>, params: {app,
   review_id, text}, playbook: "reply-to-every-review"} - **0**. It returns the action id, the
   before → after diff (an existing reply shows as `before`) and the guardrail result.
   A `BLOCKS` check (e.g. over 350 characters on Play) means: shorten or fix and propose again.
6. Show the user one table of all drafts (see Output format), flagged ones first, and ask which to
   post: "all", "all except 3, 7", or edits ("4: mention the export fix"). Re-propose edited ones.
7. For each approved row: `apply_action` {id} - **1 when posted**. Outcomes:
   - `applied`: posted (App Store replies appear after Apple's review, usually within 24 h).
   - `pending_approval`: the org requires a person to approve in the dashboard; collect the
     `approve_url`s and give them to the user (one link per action, or https://dash.appgoat.ai/approvals).
   - "needs approval by a person" (403): same, hand over the link, do not retry.
   - "account changed" (409): someone replied meanwhile; show the new diff and skip unless the user
     wants to replace it (`force: true`).
8. `reject_action` {id, reason} - **0** for drafts the user declined, so they leave the approvals list.
9. Report what was posted, what waits for approval and what was skipped.

Budget: **1–3 credits** to read + **1 per posted reply** (dry runs and pending approvals are free).

## Decision rules

- **Answer the review, not a template.** Reference one or two concrete points the user made
  (the feature, the bug, the version). Never copy the same reply across reviews.
- **Length:** 2–4 sentences. Play replies ≤ 350 characters (hard limit); App Store ≤ 600 as a
  house rule (limit 5970). Count before proposing.
- **Negative (1–2★):** thank, acknowledge the specific problem without arguing, give one concrete
  next step (update to the version with the fix if the user confirmed one, a setting, or the
  support address). Ask for details only through the support channel.
- **Neutral (3★):** thank, answer the question or suggestion, say if it is on the roadmap only if
  the user confirmed it.
- **Positive (4–5★):** thank them for something specific; one sentence is fine. No upsell.
- **Never:** promise dates, refunds, features or fixes the user did not confirm; offer incentives
  for changing the rating (against both stores' policies); ask for a better rating; include
  personal data (names, emails, order ids) of the reviewer or staff; blame the user or Apple/Google;
  link anywhere but the app's own support or privacy pages.
- **Skip** (do not reply, list them): spam, abusive reviews, reviews that are only a star with no
  text on Play, and legal threats (flag those to the user).
- **Guardrail:** `flagged` or any check under 0.7 → rewrite once before showing it; if still
  flagged, show it with the flag and let the user decide. Never apply a draft whose guardrail shows
  `BLOCKS`.
- **Existing replies:** this playbook only answers unanswered reviews; replacing a reply needs the
  user to ask for it.

## Output format

Draft table (before step 7):

```markdown
# Review replies: <app> (<store>) - <n> unanswered, <k> drafted

| # | ★ | Review (excerpt) | Reply draft | Chars | Guardrail | Action |
|---|---|---|---|---|---|---|
| 1 | 1 | "Login loops forever since 2.4…" | "Sorry about the login loop since 2.4…" | 212 | flagged: claims 0.62 (promises a fix) | act_… |
| 2 | 5 | "Love the widgets" | "Thank you! The widgets are…" | 96 | passed 0.95 | act_… |

Skipped: 2 spam, 1 legal threat (#14, please read it yourself).
Reply "post all", "post all except 1", or edit a row.
```

Run report (after step 7):

```markdown
Posted 18 replies (App Store replies go live after Apple's review).
Waiting for approval in the dashboard (4): https://dash.appgoat.ai/approvals
Skipped 3, rejected 2 drafts. Credits used: <sum>.
```

## Automate it

Daily drafts that a person approves in the AppGoat dashboard. The run calls `apply_action` once per
draft, which submits it for approval (or posts it when the org has a Studio auto-apply rule for
`review.reply` that the guardrail score clears). Without such a rule nothing is posted until
someone approves it at https://dash.appgoat.ai/approvals.

GitHub Action (`.github/workflows/appgoat-review-replies.yml`, secrets `ANTHROPIC_API_KEY`, `APPGOAT_API_KEY`):

```yaml
name: AppGoat review replies
on:
  schedule:
    - cron: "0 7 * * *"
  workflow_dispatch:
permissions:
  contents: read
jobs:
  replies:
    runs-on: ubuntu-latest
    steps:
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
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Use the reply-to-every-review skill for all linked apps. This is an unattended run: use a friendly,
            plain voice and the support URL from the listing, promise nothing. Instead of asking the user in step 6,
            call apply_action once for every draft whose guardrail passed (this submits it for approval in the
            dashboard), and reject_action the rest with the reason. Never call apply_action with force.
          claude_args: |
            --mcp-config ${{ runner.temp }}/appgoat-mcp.json
            --allowedTools mcp__appgoat__list_connections,mcp__appgoat__read_connection,mcp__appgoat__get_reviews,mcp__appgoat__propose_action,mcp__appgoat__apply_action,mcp__appgoat__reject_action,mcp__appgoat__get_action
```

Claude Code routine:

```text
/schedule weekdays 09:00 - Run the reply-to-every-review playbook for my linked apps. Draft replies, submit the ones whose guardrail passed for approval (apply_action once each), and send me the approvals link with a one-line summary per app.
```
