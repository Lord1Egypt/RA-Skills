# Environment Check (Step 1)

The agent executes the checks below step by step, making decisions based on each result in real time. Run CLI commands directly.

---

## 1. CLI Installed?

```bash
aliyun version 2>&1 | head -1
```

| Result | Action |
|--------|--------|
| Version output (e.g. `3.x.x`) | Continue |
| command not found | Tell user to install (see below) |
| Version < 3.x | Tell user to upgrade |

**CLI Installation**: Tell the user to install it using the official guide:
- https://www.alibabacloud.com/help/en/cli/install-update-alibaba-cloud-cli

---

## 2. Credential Check

```bash
aliyun configure list 2>&1
```

Look for the default profile line (marked with `*`):

| Result | Action |
|--------|--------|
| `*` line present and contains `Valid` | Credential valid, skip to step 3 |
| `*` line present but not `Valid` | Expired/invalid, enter **Auth Flow** |
| No `*` line / command errors (config.json missing) | No credential, enter **Auth Flow** |

---

## Auth Flow

**Must ask the user via chat to choose auth method first.** Recommend OAuth (more secure, no key management):

> Authentication is needed. Please choose a method:
> 1. **OAuth browser login (Recommended, more secure)** — no key management, just one click
> 2. **AK/SK manual configuration** — you manage AccessKeys yourself

### User Chooses OAuth

Run the following two commands in sequence:

```bash
# Auto pre-write config (site, region, language) — no user action needed
aliyun configure set --mode OAuth --profile default \
  --oauth-site-type INTL --region ap-southeast-1 --language en
```

```bash
# Opens the browser for user authorization
aliyun configure --mode OAuth --profile default
```

After executing the second command, tell the user: "A browser has been opened. Please click 'Authorize' in the browser."

Once authorization is complete, re-run `aliyun configure list` to verify the credential is Valid.

### User Chooses AK/SK

Tell user to run in their own terminal:

```
aliyun configure --profile default
```

Remind them:
- Use region `ap-southeast-1`
- **Never paste keys into chat**

After user confirms configuration is done, re-run `aliyun configure list` to verify.

---

## 3. Region Confirmation

```bash
aliyun configure get region 2>&1
```

| Result | Action |
|--------|--------|
| Has value (e.g. `ap-southeast-1`) | Record as REGION, continue |
| Empty | Use default `ap-southeast-1`, continue |

---

## 4. OSS Service Activation Check

```bash
aliyun oss ls 2>&1
```

| Result | Action |
|--------|--------|
| Normal output (bucket list or empty) | OSS activated, continue |
| Contains `not activated` / `NoSuchService` / `未开通` | Auto-activate ↓ |

Auto-activate:

```bash
aliyun ossadmin OpenOssService 2>&1
```

Re-verify with `aliyun oss ls` after. If still unavailable, tell user to activate manually: https://oss.console.aliyun.com/

---

## 5. Identity Probe

```bash
aliyun sts GetCallerIdentity 2>&1
```

| Result | Action |
|--------|--------|
| Returns JSON with `AccountId` and `Arn` | Record ACCOUNT_ID and ARN, check passed ✓ |
| Error | OAuth likely expired — guide user back to Auth Flow |

> The minimal RAM permissions for deployment are in `reference/rules/ram_policies.md`; on a
> `Forbidden.RAM` error, cross-check that table to grant the missing action.

---

## Outputs After Check

Once all checks pass, the agent holds these variables for subsequent steps:

- `REGION` — deploy region (default `ap-southeast-1`)
- `ACCOUNT_ID` — Alibaba Cloud account ID
- `IDENTITY_ARN` — caller ARN

---

## Secret Leak Guard

The host AI agent may persist approved commands and history to disk, capturing
AK/SK, passwords, or OSS signed URLs.

- Never pass AK/SK or passwords as command arguments or into chat; use env vars.
- Step 13 adds the agent's workspace dirs to `.gitignore`.
- If such a file is already tracked, tell the user to `git rm --cached` it and rotate the exposed credential.
