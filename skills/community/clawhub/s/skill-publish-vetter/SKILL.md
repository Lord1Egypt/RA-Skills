---
name: skill-publish-vetter
version: 1.1.0
description: Pre-publish privacy scan for ClawHub skills. Detects tokens, keys, credentials, .env secrets, personal info, and internal IPs before publishing.
---

# Skill Publish Vetter 🛡️

Pre-publish privacy scan for ClawHub skills.

**Every skill must pass this scan before publishing to ClawHub.**

---

## When to Use

- User says "publish skill to ClawHub"
- User says "upload skill to ClawHub"
- User says "update skill on ClawHub"
- Any request to submit a skill to a public registry

---

## Core Principle

**Publishing to ClawHub = publicly visible. Any leaked secret is exposed to the world.**

Better safe than sorry. **Even if the scan passes, always ask for user confirmation before publishing.**

---

## Publish Workflow (Mandatory)

When the user requests a publish/upload/update to ClawHub, **follow these steps strictly**:

### Step 1: Identify the Target Skill

- If the context clearly identifies the target skill, proceed.
- Otherwise, ask the user which skill to publish.

### Step 2: Run the Privacy Scan

The scan script lives in this skill's `scripts/publish-check.sh`. Run it from this skill's directory:

```bash
bash scripts/publish-check.sh <target-skill-directory>
```

It scans for:

| Category | Detection Pattern | Example |
|----------|-------------------|---------|
| **Tokens / Keys** | `sk-`, `ghp_`, `github_pat_`, `gpg_`, `xoxb-`, `glpat-`, JWT tokens | `sk-abc123...` |
| **API Keys** | `api_key`, `apikey`, `API_KEY`, `access_token` with actual values | `API_KEY=abc123` |
| **Passwords** | `password`, `passwd`, `pwd` with non-placeholder values | `password=mysecret123` |
| **Private Keys** | `BEGIN.*PRIVATE KEY` | PEM private key |
| **Public Keys** | `BEGIN.*PUBLIC KEY`, `ssh-rsa` long strings | SSH public key |
| **`.env` Values** | `.env` files with actual (non-placeholder) assignments | `.env: DB_PASS=real_password` |
| **Hardcoded Creds** | `Authorization: Bearer` with real tokens | `curl -H "Authorization: Bearer sk-xxx"` |
| **Personal Emails** | Non-placeholder, non-org emails | `zhangsan@gmail.com` |
| **Personal Paths** | `/home/username/`, `/Users/username/` absolute paths | `/Users/weidongkl/.ssh/id_rsa` |
| **Internal IPs** | `192.168.x.x`, `10.x.x.x`, `172.16-31.x.x` | `https://192.168.1.100:8080` |

### Step 3: Output the Full Report

**Output the complete scan report to the chat.** Do not summarize or omit anything.

### Step 4: Secondary Confirmation (Required)

**Always** ask for confirmation before publishing — even if the scan is clean.

Confirmation message must include:

1. **Skill name**
2. **Skill directory path**
3. **Full scan report**
4. **A clear confirmation prompt**

Template:

```
📋 Publish Confirmation

Skill: <name>
Path: <directory>
Version: <version>
Scan Result: <PASS / ISSUES FOUND>

[Full report here]

Reply "yes" or "confirm" to proceed with publishing, or "cancel" to abort.
```

### Step 5: Wait for User Response

- "yes" / "confirm" / "ok" / "go" → proceed to Step 6.
- "cancel" / "no" / "stop" → abort. Do nothing.
- No response → do not publish. Wait.

**Never skip confirmation. Never auto-publish.**

### Step 6: Publish

After confirmation:

```bash
clawhub publish <skill-directory> --slug <slug> --name "<name>" --version "<version>" --changelog "<changelog>"
```

Ask the user for slug, name, version, and changelog if not provided.

### Step 7: Report Result

Tell the user whether publishing succeeded or failed.

---

## Risk Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🚨 **CRITICAL** | Token, key, password, private key with actual values | **Block publish.** User must fix first. |
| ⚠️ **WARNING** | Personal email, personal path, internal IP | **Recommend fixing** before publishing. |
| 💬 **INFO** | author, repository identity fields, metadata env exposure | **Ask user** if intentionally public. |

---

## Red Lines (Auto-Block)

If any of these are found, **refuse to publish by default**:

1. Any token with actual values (Bearer tokens, API keys, Access tokens)
2. Any private key content (PEM format, SSH private keys)
3. Any password/credential with actual values (not placeholders)
4. `.env` files with actual configuration values
5. Hardcoded internal IPs or domains
6. Base64-encoded sensitive data

If the user explicitly says "publish anyway despite risks", re-confirm once before proceeding.

---

## Placeholder Reference

Use these placeholders when fixing issues:

| Type | Placeholder |
|------|-------------|
| Token | `your-api-token` / `<YOUR_TOKEN>` |
| API Key | `your-api-key` / `<API_KEY>` |
| Password | `your-password` / `<PASSWORD>` |
| Email | `you@example.com` / `<YOUR_EMAIL>` |
| Username | `your-username` / `<USERNAME>` |
| URL | `https://your-server.example.com` |
| IP | `your-server-ip` |

---

## Scan Script

The script is at `scripts/publish-check.sh` relative to this skill's directory. It uses no absolute paths and works in any installation location.

```bash
bash scripts/publish-check.sh <target-skill-directory>
```

---

*Safety first, publishing second. Never publish without confirmation.* 🛡️
