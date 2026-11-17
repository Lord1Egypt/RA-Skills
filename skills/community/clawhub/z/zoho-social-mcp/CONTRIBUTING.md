# Contributing

Contributions from humans and agents are explicitly welcome. Daily use is the discovery loop: every reproducible defect, missing capability, safer check, or useful simplification belongs upstream.

Do **not** add a wrapper script for GitHub. Use native `git` and `gh`. If something in this skill is wrong, incomplete, or unsafe, report it immediately and keep going.

## Workflow

1. Search open issues first:
   ```bash
   REPO=sprintberlin/openclaw-zoho-social-mcp-skill
   gh issue list --repo "$REPO" --state open --search "<terms>"
   ```
2. If a matching issue exists, link it. Otherwise create one immediately:
   ```bash
   gh issue create --repo "$REPO" \
     --title "<short imperative summary>" \
     --body "<sanitized requirement, actual vs. expected behavior, and acceptance criteria>"
   ```
3. If implementation is feasible now, deliver it end-to-end:
   ```bash
   git switch -c "<type>/<short-name>"
   python3 -m unittest discover -s tests -v
   git add <files>
   git commit -m "<conventional commit message>" -m "Closes #<issue>"
   git push -u origin HEAD
   gh pr create --repo "$REPO" --base main --title "<title>" --body "Closes #<issue>"
   gh pr checks --repo "$REPO" --watch
   gh pr merge --repo "$REPO" --squash --delete-branch
   git switch main && git pull --ff-only
   ```
4. If implementation is not feasible now, filing the issue is mandatory. Return the issue URL.
5. Never leave uncommitted repository changes behind. A task is only complete when `main` is clean, or when the PR URL and blocker are explicitly reported.

## Rules

- Never include secrets, MCP URLs, tokens, customer names, portal IDs, brand IDs, channel IDs, post IDs, or live filenames in issues, PRs, or commit messages.
- Confirm the live MCP server with `mcporter list` before relying on an Action. The catalog describes possible Actions, not a particular connection.
- Local image uploads must send the complete `data:image/...;base64,...` payload. Truncated base64 is a failed upload even if MCP reports success.
- Treat an empty media or post response as failure. Re-list the library or post after writes.
- CI runs unit tests only. Never make live network calls from GitHub Actions.
- Keep `SKILL.md` compact and imperative for agents. Put deeper explanations in `README.md`.

## Docs to update with a change

- `README.md` / `SKILL.md` if helper usage, profiles, or media rules change
- `references/actions.jsonl` and `references/profiles.json` if Zoho changes the catalog
- `package.json` version and `skill-card.md` for a public release
