---
name: qqmail-organizer
description: Agent-facing QQ Mail inbox management over IMAP/SMTP for OpenClaw, Hermes, and other autonomous agents. Use when an agent must read, search, reply to, classify, organize, archive, mark read/unread, or safely clean up a QQ Mail inbox while preserving explicit dry-run/approval boundaries. Especially useful for agentic inbox triage, non-mutating cleanup plans, rule-based organization, newsletter/marketing/GitHub notification sorting, and avoiding accidental destructive email operations.
---

# QQMail Organizer

## Agent Contract

Use this skill as an execution protocol for agents, not as a human walkthrough. The agent should operate the bundled scripts, summarize results, preserve safety boundaries, and avoid exposing credentials or unnecessary private email content.

Core behavior:

- Prefer deterministic script calls over hand-written IMAP/SMTP snippets.
- Prefer `--json` for parent-agent orchestration when using `plan-organize` or `auto-organize`.
- Treat `plan-organize` and default `auto-organize` as safe read-only planning.
- Treat `--apply`, `archive` without `--dry-run`, `mark-*` without `--dry-run`, `send` without `--dry-run`, `reply` without `--dry-run`, and `delete` as mutations.
- Require explicit user approval before destructive or externally visible actions.
- Report concise summaries, matched counts, categories, and proposed actions instead of dumping full inbox content.

Credentials are read only from environment variables:

- `QQMAIL_USER`: QQ email address.
- `QQMAIL_AUTH_CODE`: QQ Mail IMAP/SMTP authorization code, not the account password.

Never print, persist, or place `QQMAIL_AUTH_CODE` in prompts, reports, cron jobs, memory, commits, or rule files.

## Decision Protocol

1. For "look at my mail", "what is important", "clean my inbox", or ambiguous organization requests, start with:

```bash
python3 scripts/qqmail.py plan-organize --limit 50 --json
```

2. For rule-based cleanup, preview first. This is dry-run by default:

```bash
python3 scripts/qqmail.py auto-organize --limit 100 --json
```

3. Apply only after the user explicitly confirms the rule/action set:

```bash
python3 scripts/qqmail.py auto-organize --limit 100 --apply
```

4. For a specific requested move, mark, send, or reply, run a narrow command. Use `--dry-run` first for bulk move/mark/delete operations.

5. For permanent deletion, do not infer intent. Ask or require explicit wording such as "delete permanently".

## Output Protocol

When reporting to a user or parent agent:

- State whether the operation was read-only, dry-run, or applied.
- Group results by category or action.
- Include sender, subject, date, and count. Avoid full body content unless the user asks to read a specific message.
- For parent agents, parse `--json` output instead of scraping human-readable text.
- For dry-run cleanup, list the exact actions that would occur and the command needed to apply them.
- If credentials, IMAP, or SMTP fail, report the failing boundary without printing secrets.

## Commands For Agents

Read and inspect:

```bash
python3 scripts/qqmail.py folders
python3 scripts/qqmail.py inbox --limit 20
python3 scripts/qqmail.py inbox --unread --limit 20
python3 scripts/qqmail.py read --index 1
python3 scripts/qqmail.py search --from "sender@example.com"
python3 scripts/qqmail.py search --subject "keyword" --since "2026-06-01"
```

Send and reply:

```bash
python3 scripts/qqmail.py send --to "recipient@example.com" --subject "Hello" --body "Message" --dry-run
python3 scripts/qqmail.py send --to "recipient@example.com" --subject "Hello" --body "Message"
python3 scripts/qqmail.py reply --index 1 --body "Reply text" --dry-run
python3 scripts/qqmail.py reply --index 1 --body "Reply text"
```

Organize safely:

```bash
python3 scripts/qqmail.py plan-organize --limit 50 --json
python3 scripts/qqmail.py auto-organize --limit 100 --json
python3 scripts/qqmail.py mkdir "GitHub"
python3 scripts/qqmail.py archive --from "notifications@github.com" --target "GitHub" --dry-run
python3 scripts/qqmail.py mark-read --index 1 --dry-run
python3 scripts/qqmail.py mark-unread --from "sender@example.com" --dry-run
```

Delete is available but should be used only after explicit user confirmation:

```bash
python3 scripts/qqmail.py delete --index 1 --dry-run
python3 scripts/qqmail.py delete --index 1 --confirm-delete DELETE
```

## Rules

Rule-based organization uses `rules.agent.json` by default. This default policy intentionally contains no rules, so packaged skill behavior never archives, marks, or moves mail based on public sample preferences. Agents should generate or select an explicit `--rules /path/to/rules.json` only after the user has approved the mailbox policy.

Use `rules.schema.json` as the machine-readable contract for generated policy files. The script also validates rules before planning or applying them.

Rules support matching by sender, subject, or inferred category, and actions such as:

- `archive`: copy to a target folder, then remove from source.
- `mark-read`: add the `Seen` flag.
- `mark-unread`: remove the `Seen` flag.
- `review`: classify only, do not mutate.

For personalized cleanup, write a private rules file outside the public skill repo and call:

```bash
python3 scripts/qqmail.py validate-rules --rules /path/to/rules.json --json
python3 scripts/qqmail.py auto-organize --rules /path/to/rules.json --limit 100 --json
python3 scripts/qqmail.py auto-organize --rules /path/to/rules.json --limit 100 --apply --json
```

Only run the `--apply` command after the user approves the exact action set from the dry-run JSON.

## Safety Policy For Agent Runtimes

- Prefer `plan-organize` before any mutation.
- Use `--dry-run` for manual archive, delete, and mark operations before applying.
- `auto-organize` is dry-run unless `--apply` is present.
- Use `send --dry-run` and `reply --dry-run` before externally visible messages unless the user already approved the exact content.
- `delete` refuses to run without `--confirm-delete DELETE`; still require explicit user approval first.
- Never run `delete` unless the user explicitly asks for permanent deletion.
- Never create automatic reply, delete, or archive cron jobs without explicit user confirmation.
- Do not log or commit QQ Mail authorization codes.
- Do not use this skill as a background auto-responder without a human-approved policy.
- Do not treat marketing/newsletter classification as permission to delete.
