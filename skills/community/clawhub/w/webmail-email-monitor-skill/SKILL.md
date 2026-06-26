---
name: webmail-email-monitor
description: |
  Monitor Outlook and other common webmail inboxes in a persistent Edge
  profile, process new messages as a detached local background task, capture
  complete message screenshots, download attachments to the desktop, and write
  structured Excel rows with deterministic Python logic. Use when Codex needs
  to start, stop, verify, or modify a Windows email monitoring workflow.
---

# Webmail Email Monitor

Run this skill as a local background process on Windows.

## Operating mode

Treat supported webmail monitoring as a detached automation task, not as an
in-turn browser session.

Do this by default:

- Start the monitor with `powershell -ExecutionPolicy Bypass -File scripts/webmail_monitor_cli.ps1 start`
- Tell the user that mailbox login, if needed, must be completed in one of the
  opened Edge windows
- Report that the monitor keeps running after the current chat turn ends
- Check `powershell -ExecutionPolicy Bypass -File scripts/webmail_monitor_cli.ps1 status`
  or `powershell -ExecutionPolicy Bypass -File scripts/webmail_monitor_cli.ps1 logs`
  if the user asks whether it is running

Do not do this by default:

- Try to keep Outlook open by holding the current chat turn forever
- Manually drive a mailbox login page as the primary execution path
- Stop the monitor unless the user explicitly asks to stop it

## Standard rule

Prefer Python over prompt logic whenever the work can be expressed
deterministically.

Use prompt text for orchestration, brief user communication, and the small set
of judgments that truly require semantic interpretation.

Move the rest into scripts.

## Fast return rule

When the user asks to start or enable monitoring, do not keep the current chat
turn open waiting for mailbox login, message opening, attachment processing, or
Excel writes.

Use this exact success path:

1. Run `powershell -ExecutionPolicy Bypass -File scripts/webmail_monitor_cli.ps1 start`
2. Run `powershell -ExecutionPolicy Bypass -File scripts/webmail_monitor_cli.ps1 status`
3. If status is `running`, return immediately

Do not block the reply on:

- Completing Gmail or other mailbox login
- Waiting for the first polling cycle to finish
- Waiting for screenshots, attachment downloads, or Excel writes
- Tailing logs unless the user explicitly asks for logs or troubleshooting

## Python-first boundary

Keep these behaviors in Python scripts instead of prompt instructions:

- Browser session recovery and persistent profile reuse
- Inbox polling, retry logic, timeout handling, and recovery
- Process lifecycle, PID tracking, and runtime logging
- Message deduplication and processed-state storage
- Reconciliation between processed-state storage and the Excel workbook
- Message opening, body extraction, and sender or subject capture
- Date parsing, designer extraction, style-code extraction, and other fixed
  field rules
- Excel workbook creation, formatting, row writing, image embedding, and file
  naming
- Complete-message screenshots and screenshot path management
- Attachment detection, download handling, deduplication, and desktop saving
- Best-effort attachment content extraction for common file types before Excel
  writing
- Any repeatable transformation that can be implemented with rules, regex, or
  explicit conditionals

Do not rewrite deterministic Python behavior as a natural-language checklist
inside the skill.

## Model boundary

Only use model judgment for work that cannot be expressed reliably in Python,
such as:

- Interpreting ambiguous request language from the user
- Resolving genuinely fuzzy business meaning from a message when fixed rules
  are insufficient
- Producing a short human-readable summary when deterministic extraction is not
  enough

If a behavior can be implemented with explicit rules, implement or update the
Python script instead of expanding the prompt.

## Required output behavior

Make the monitor produce these local artifacts:

- A desktop workbook named `outlook_email_monitor.xlsx`
- A desktop screenshots folder named `outlook_email_monitor_shots`
- Downloaded mail attachments saved to the desktop
- A runtime log at `runtime/monitor.log`

Make the workbook row structure match the existing business table in this
column order:

- Creation date
- Creator
- Manual or independent request type
- Email subject
- Requested completion time
- Content summary
- Related image
- Designer
- Other related information
- Revision notes
- Selected style

Capture the full visible message content whenever possible. If the page cannot
produce a full-page screenshot, capture the most complete fallback screenshot
available and keep processing.

Download visible attachments whenever they are present and record their names
or related notes in the workbook.

Read supported attachment content with Python after download and feed that
content into the same deterministic field-extraction rules before writing the
Excel row. If a file type cannot be read reliably, still download it, record
its filename, and keep processing.

Only treat an email as fully processed after the Excel write succeeds. If the
processed-state marker exists but the workbook row is missing, the monitor must
rewrite the row instead of skipping it.

Support the same workflow across Outlook and other common webmail providers.
Prefer built-in support for Outlook, Gmail, QQ Mail, 163 Mail, 126 Mail, and
Yahoo Mail, then fall back to generic browser-mail selectors when possible.
Use Gmail as the default monitored provider unless the user explicitly asks to
switch to a different mailbox.

## Start

```powershell
powershell -ExecutionPolicy Bypass -File scripts/webmail_monitor_cli.ps1 start
```

After the first start:

- Finish mailbox login in the opened Edge window or the relevant seeded mail
  tab
- Keep that Edge profile for future runs
- The CLI auto-runs a bootstrap step that installs missing Python dependencies
  and refreshes the local `webmail-monitor` shim
- The bootstrap step also detects missing Python or Microsoft Edge and attempts
  to install them automatically with `winget`

## Reuse requirements

Keep this skill reusable across machines by following these rules:

- Keep all execution logic in the skill folder and its scripts
- Avoid machine-specific hardcoded paths in `SKILL.md`
- Resolve runtime paths relative to the skill root inside scripts
- Expose one explicit command surface for operators, currently `webmail-monitor`
- If the skill is copied to another machine, recreate the local command shim so
  `webmail-monitor` points to that machine's copied skill folder
- Make the bootstrap step idempotent so OpenClaw can safely run it on first use

Assume these host prerequisites for reuse:

- Windows with PowerShell available
- A writable Desktop path for the workbook, screenshots, and downloaded
  attachments
- OpenClaw configured to scan the workspace `skills/` directory
- Either existing Python and Microsoft Edge, or a host that allows automatic
  installation through `winget`

If a prerequisite is missing, report the missing requirement directly instead of
pretending monitoring started successfully.

OpenClaw should rely on the bootstrap-capable CLI script so first-run dependency
installation can happen automatically on a new machine.

Bootstrap responsibilities on a new machine:

- Detect Python and install it automatically if missing
- Detect Microsoft Edge and install it automatically if missing
- Install required Python packages for the monitor scripts
- Recreate or update the local `webmail-monitor` command shim

If automatic host installation is blocked because `winget` is unavailable or
restricted, fail with explicit manual install URLs instead of pretending the
machine is ready.

## Stop

```powershell
powershell -ExecutionPolicy Bypass -File scripts/webmail_monitor_cli.ps1 stop
```

## Status and logs

```powershell
powershell -ExecutionPolicy Bypass -File scripts/webmail_monitor_cli.ps1 bootstrap
powershell -ExecutionPolicy Bypass -File scripts/webmail_monitor_cli.ps1 doctor
powershell -ExecutionPolicy Bypass -File scripts/webmail_monitor_cli.ps1 status
powershell -ExecutionPolicy Bypass -File scripts/webmail_monitor_cli.ps1 logs
webmail-monitor status
webmail-monitor logs
```

## Default workflow

Follow this workflow when monitoring is requested:

1. Start the detached monitor.
2. Confirm monitoring from `powershell -ExecutionPolicy Bypass -File scripts/webmail_monitor_cli.ps1 status`.
3. Ask the user to complete mailbox login in the opened Edge window if needed.
4. Leave the background process running after the chat turn ends.
5. Stop the monitor only when the user explicitly asks.

## Response pattern

After starting the monitor, respond with a short status update that includes:

- That the background monitor has been started
- That Edge may open one or more mailbox tabs for login
- That login only needs to be completed in the persistent profile window
- That future polling continues outside the current chat turn
- That detailed progress belongs to the CLI `logs` command, not the start flow

After stopping the monitor, confirm that the background process has been
stopped.

## Notes

- The launcher is detached on purpose so the browser does not close when the
  OpenClaw agent turn ends.
- If a mailbox asks for login again, complete it once in the persistent Edge
  profile and later runs should reuse that session.
- When the user asks to change extraction behavior, prefer patching the Python
  monitor script over adding more prompt prose.
- The portable invocation path is the relative CLI script under `scripts/`.
- Prefer the explicit command surface `webmail-monitor start|stop|restart|status|logs`
  over direct script paths.
- `webmail-monitor start` should be treated as a fire-and-return action, not a
  long-running foreground task inside the chat turn.
- If `processed.json` says a mail was handled but the workbook does not contain
  the corresponding row, treat that as recoverable state drift and rewrite the
  row.
