---
name: waha-onboarding
description: Onboard a new user to WhatsApp via WAHA—greet them, collect and sanitize their phone number, create/start a WAHA session, request and share a pairing code, verify authentication, and then offer next actions (recent chats, contacts, specific chat).
---

# WAHA Onboarding Skill

Use this skill when a user wants to connect their WhatsApp account through WAHA.

## Onboarding flow

### 1) Collect phone number

Ask for the user’s WhatsApp number including country code.

Example prompt:

"👋 I can connect your WhatsApp. Send your phone number with country code (digits only if possible), for example `905380546393`."

### 2) Sanitize number and derive session name

- Strip all non-digit characters from the input.
- Use sanitized value as `<phonenumber>`.
- Session name format: `user-<phonenumber>`.

### 3) Create and start WAHA session

Run:

```bash
waha-cli waha-create-session --name user-<phonenumber>
sleep 5
waha-cli waha-start-session --session user-<phonenumber>
```

### 4) Request pairing code

Run:

```bash
sleep 5
waha-cli waha-request-pairing-code --session user-<phonenumber> --phone-number <phonenumber>
```

### 5) Share pairing instructions

Send the returned code and tell user:

1. Open WhatsApp → **Linked Devices**
2. Tap **Link a Device**
3. Tap **Link with phone number instead**
4. Enter the pairing code

### 6) Verify authentication after user confirms

Run:

```bash
waha-cli waha-check-auth-status --session user-<phonenumber>
```

- If status is `WORKING`: onboarding succeeded.
- Otherwise: run fallback.

### 7) Confirm success and offer next actions

Offer:

- recent conversations
- contacts
- messages from a specific chat

## Fallback (if not WORKING)

Restart and issue a fresh code:

```bash
waha-cli waha-start-session --session user-<phonenumber>
sleep 8
waha-cli waha-request-pairing-code --session user-<phonenumber> --phone-number <phonenumber>
```

Then ask user to retry from WhatsApp Linked Devices.

## Naming and ID conventions

- WAHA session: `user-<phonenumber>`
- Direct chat id convention: `<phonenumber>@c.us`
