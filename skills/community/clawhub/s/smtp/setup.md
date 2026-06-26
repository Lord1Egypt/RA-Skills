# Setup - SMTP

Use this file when `~/smtp/` is missing, empty, or clearly stale.

Answer the immediate SMTP question first, then install the minimum safe context so future tests do not repeat risky guesses.

## Immediate First-Run Actions

### 1. Lock the operating mode

Clarify which of these is actually needed:
- draft-only help
- connectivity or TLS probe
- auth probe
- canary send to one approved inbox
- real send to external recipients

Default to the safest mode that still answers the user's question.

### 2. Lock provider and sender identity context

Confirm the smallest useful set of facts:
- SMTP host and port
- TLS mode: implicit TLS, STARTTLS, or local relay
- authenticated identity
- visible From address and return-path expectation
- whether the user controls the sender domain

Do not ask for passwords in chat.

### 3. Lock live-send boundaries

Before any live message:
- ask whether a canary inbox is available
- ask whether external recipients are allowed
- ask whether the first test must stay plain text and one-recipient only
- ask how success should be verified: queue response, inbox, spam folder, or provider logs

Default to one-recipient canary mode.

### 4. Lock credential handling

Credentials should come from a secret manager, runtime prompt, or short-lived environment already approved by the user.

Never store raw credentials in:
- `~/smtp/memory.md`
- `~/smtp/provider-profiles.md`
- `~/smtp/send-log.md`
- `~/smtp/deliverability-notes.md`

### 5. Create local state only after the safety path is clear

```bash
mkdir -p ~/smtp
touch ~/smtp/{memory.md,provider-profiles.md,send-log.md,deliverability-notes.md}
chmod 700 ~/smtp
chmod 600 ~/smtp/{memory.md,provider-profiles.md,send-log.md,deliverability-notes.md}
```

If the files are empty:
- initialize `~/smtp/memory.md` from `memory-template.md`
- initialize `~/smtp/provider-profiles.md` from `provider-profiles.md`
- initialize `~/smtp/send-log.md` from `send-log.md`
- initialize `~/smtp/deliverability-notes.md` from `deliverability-notes.md`

### 6. What to save

Save only context that improves future SMTP work:
- approved provider hosts and ports
- known-good TLS and auth combinations
- sender-identity and domain-alignment notes
- canary inbox choice and live-send boundaries
- queue IDs, bounces, and placement evidence worth remembering

Do not store raw secrets, full message bodies by default, or recipient lists that do not need durable logging.
