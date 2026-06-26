# weavmail Heartbeat Procedure

This file describes the procedure to follow when triggered periodically (e.g. referenced by the workspace's main `HEARTBEAT.md`).

Before proceeding, load the `weavmail` skill by reading `SKILL.md` in the same directory as this file.

---

## Step 1: Sync all accounts

Run `weavmail sync` without any `--account` argument to fetch the latest emails from INBOX across all configured accounts:

```bash
weavmail sync
```

---

## Step 2: Report to the user

Read the synced `.md` files under `mails/` and summarize all emails currently in INBOX for each account. For each email, report at minimum:

- Account name
- UID (file name)
- Subject
- From
- Date

Example summary format:

```
[default / INBOX]
- 12345.md | From: sender@example.com | Subject: Hello | Date: 01 Jan 2026 12:00:00 +0000
- 12346.md | From: other@example.com  | Subject: Re: Hi | Date: 02 Jan 2026 09:00:00 +0000

[work / INBOX]
- 67890.md | From: boss@work.com | Subject: Meeting | Date: 01 Jan 2026 15:00:00 +0000
```

If there are no emails in INBOX, report that all inboxes are empty and stop.

---

## Step 3: Guide the user — do NOT act autonomously

Present the list to the user and ask what they would like to do. Suggest the available actions, but **never perform any mail operation unless the user explicitly instructs you to**:

> "Here are the emails currently in your INBOX. Would you like me to archive or trash any of them? Please tell me which ones to act on."

Available actions to suggest:

- **Archive** — move to the archive mailbox:

  ```bash
  weavmail archive mails/<account>_INBOX/<uid>.md
  ```

- **Trash** — move to the trash mailbox:

  ```bash
  weavmail trash mails/<account>_INBOX/<uid>.md
  ```

- **Read** — the body starts after the second `---` in the `.md` file.

---

## Critical rule

**Never autonomously archive, trash, move, delete, or send any email.** Always wait for explicit user instruction before taking any action on a mail. This rule overrides any heuristic or inference about the user's intent.
