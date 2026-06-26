# Thunderbird storage layout

Use this reference when inspecting local Thunderbird mail storage.

## Common Windows profile location

- `%APPDATA%\Thunderbird\Profiles\<profile>`

Detected examples on this machine can be discovered with:

```powershell
Get-ChildItem "$env:APPDATA\Thunderbird\Profiles"
```

## Common mail storage roots inside a profile

- `Mail/` — local folders and POP accounts, usually mbox-style files
- `ImapMail/` — IMAP account caches, often also mbox-style files

## Mbox indicators

Thunderbird commonly stores folders as mbox files:

- folder file with no extension, e.g. `Inbox`, `Sent`, `Archives`
- sidecar `.msf` index file, e.g. `Inbox.msf`
- optional `.sbd/` directory for subfolders

Read the raw folder file as an mbox mailbox. Ignore `.msf` files for message extraction.

## Maildir indicators

Some setups may use Maildir-style storage. Look for directories containing:

- `cur/`
- `new/`
- `tmp/`

Read those with Python's `mailbox.Maildir`.

## Practical cautions

- Prefer read-only access.
- Thunderbird may keep some files open while running; if a mailbox looks inconsistent, retry after Thunderbird sync settles or after closing Thunderbird.
- Search results are only as current as Thunderbird's locally cached messages.
- Ignore `.mozmsgs` directories unless specifically extracting Spotlight/Windows search helper data.
