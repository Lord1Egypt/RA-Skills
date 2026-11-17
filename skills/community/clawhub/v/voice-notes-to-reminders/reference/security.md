# Security & privacy — the whole point of this tool

The value proposition is that **NerveX/NxVET only ever sees the raw voice note**. Everything the
tool *does* with a note — the calendar, the triage list, the reminders — lives on the operator's
machine and is never sent back. Protect that guarantee.

## The local-only guarantee

- The **only** outbound network calls are authenticated `GET`s to `https://app.nx.vet`.
- No telemetry, analytics, crash reporting, third-party APIs, or "phone home" of any kind.
- No reading of email/calendar over a network API in the MVP — outputs are local files only.
- If you add any new outbound call, stop and get explicit approval first. It breaks the promise.

## No send paths

- The tool produces **drafts and files** — markdown notes and `.ics` calendar files.
- It never sends an email, text, or meeting invite on anyone's behalf.
- `.ics` is deliberate: the *operator* double-clicks the file to add the event. The tool never
  talks to Outlook/Google. Adding a real send path is a separate, explicitly-approved feature.

## Secrets hygiene

- The API key (`nxvet_sk_...`) is a password. Anyone holding it can read the whole org's NxVET
  data. It can be revoked instantly from **app.nx.vet → Integrations → API Keys**.
- Store it in `.env` as `NXVET_API_KEY=nxvet_sk_...`. Nowhere else.
- If a git repo is initialized, `.env` (and `state/`, `output/`) must be in `.gitignore` before
  the first commit. Never commit the key or any clinic data.
- **Never print the full key.** When logging, mask it: show `nxvet_sk_…last4`.
- Never paste the key into a chat, ticket, or any channel that leaves the machine.
- Read the key from the environment / `.env` at runtime — never hard-code it in a script.

## Data at rest

- Transcripts and outputs contain patient/clinic-sensitive content. Keep them inside the one
  project folder. Don't sync that folder to a third-party cloud drive without the operator's
  explicit say-so.
- `state/` and `output/` are local artifacts — git-ignore them.

## If you get stuck on an API response

Save the exact request + response with the **API key and any obvious PII redacted**, and send
*that* to NerveX support. Never include a live key.

## Suggested .gitignore

```
.env
state/
output/
__pycache__/
*.pyc
```
