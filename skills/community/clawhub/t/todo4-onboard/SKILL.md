---
name: todo4-onboard
description: "Sign up for Todo4 and connect this agent via MCP. Use whenever the user says things like 'set me up with Todo4', 'sign me up for Todo4', 'install Todo4', 'connect Todo4', 'get started with Todo4', 'I want to use Todo4', 'onboard me to Todo4', or any similar request to create a Todo4 account or start using Todo4. Creates the account via email OTP and wires up the MCP connection — no browser, no password."
metadata:
  openclaw:
    bins: [curl, jq]
---

# Todo4 Onboarding Skill

This is a fixed 4-step procedure. Follow it exactly, in order, one step at a time. Do not improvise, summarize, or skip steps.

## Language

Reply in the user's language. Detect it from their messages — if they write in Thai, reply in Thai; Japanese, reply in Japanese; and so on. Default to English only if the language is unclear.

The SAY lines in each step are reference wording in English. Translate them into the user's language while preserving the meaning, the information requested, and any placeholders (e.g., `<email>`, `<WEB_LOGIN_URL>`). Do NOT translate: command output, URLs, tokens, or the literal bash scripts.

## When to run this skill

Run this whole procedure, starting at STEP 1, whenever the user asks to sign up for, install, connect, onboard, or start using Todo4. Examples of triggering requests:

- "Set me up with Todo4"
- "Sign me up for Todo4"
- "Install Todo4" / "Connect Todo4"
- "Get started with Todo4"
- "I want to use Todo4"
- "Onboard me to Todo4"

## DO NOT

- DO NOT explain what Todo4 is, list features, or ask "are you sure?" — just start STEP 1.
- DO NOT ask for more than one piece of information per message.
- DO NOT skip or combine steps.
- DO NOT continue past a failed step until the error is resolved.
- DO NOT echo the verification code, any token, or raw script JSON back to the user.

---

## STEP 1 — Ask for email

SAY (verbatim):

> I'll set you up with Todo4. I just need your email so I can send a verification code. What email should I use?

WAIT for the user's reply.

CHECK the reply contains "@" and a "." after the "@". If not, SAY: "That doesn't look like a valid email — could you try again?" and WAIT again.

Store the valid email as `<email>` and go to STEP 2.

---

## STEP 2 — Send verification code

RUN:

```bash
scripts/register.sh <email>
```

CHECK exit code:

- `0` → SAY (verbatim):
  > I've sent a 6-digit verification code to **<email>**. Please paste it here when it arrives.

  Then WAIT for the code and go to STEP 3.
- `2` and the error mentions HTTP 429 → SAY: "We've hit a rate limit. Please wait a moment and try again." STOP.
- `2` otherwise → SAY: "That email was rejected. Could you try another one?" Go back to STEP 1.
- `1` → SAY: "I couldn't reach the Todo4 server. Please check your connection and try again." STOP.

---

## STEP 3 — Verify the code

Extract the 6 digits from the user's reply as `<code>`.

**CRITICAL: Call `verify.sh` EXACTLY ONCE per code.** OTP codes are single-use — the server will reject any second call with the same code, even if the first call succeeded. Do NOT run `verify.sh` to "peek" at the output first and then again to capture. Run only the single command below, exactly once:

```bash
ACCESS_TOKEN=$(scripts/verify.sh <email> <code> | jq -r '.accessToken')
```

CHECK the exit code of the pipeline (`$?`):

- `0` and `$ACCESS_TOKEN` is non-empty → SAY: "Email verified. Connecting myself as your agent…" and go to STEP 4. **Do not re-run `verify.sh`.** `$ACCESS_TOKEN` is already captured; proceed directly to STEP 4.
- `2` → SAY: "That code didn't work. Please double-check and try again." WAIT for a new code and repeat STEP 3 with the new code. After 3 failures, SAY: "Let me send you a new code." and go back to STEP 2.
- `1` → SAY: "I couldn't reach the Todo4 server. Please check your connection and try again." STOP.

Never echo `$ACCESS_TOKEN` or the script's JSON output.

---

## STEP 4 — Connect this agent

Pick `<agent_name>` — use your own assistant name (e.g., "Claude", "GPT", "Gemini"). If unknown, use "OpenClaw".

RUN this exact command — it captures the script's stdout so you can extract the one-time web login link:

```bash
CONNECT_OUT=$(scripts/connect.sh "$ACCESS_TOKEN" <agent_name>)
```

CHECK the exit code of the pipeline (`$?`):

- `0` → the script wrote the MCP config and agent token automatically. Extract the one-time web login URL:

  ```bash
  WEB_LOGIN_URL=$(echo "$CONNECT_OUT" | grep '^WEB_LOGIN_URL=' | cut -d= -f2- | tr -d '\r\n')
  ```

  If `$WEB_LOGIN_URL` is non-empty, send the following as **three separate messages** — one per bullet, flushed individually so the user sees three distinct chat bubbles. Do NOT combine them into one message.

  1. SAY (verbatim):
     > Done — I'm connected to your Todo4 account and the MCP tools are ready.
  2. SAY (substitute the URL literally — no backticks, no code block):
     > Open your tasks in the browser — you'll be signed in automatically (link is single-use, valid for 5 minutes):
     > <WEB_LOGIN_URL>
  3. SAY (verbatim):
     > Or just tell me to create your first task — e.g., "Create a task to review the Q2 report by Friday."

  If `$WEB_LOGIN_URL` is empty, SAY (verbatim):
  > Done — I'm connected to your Todo4 account and the MCP tools are ready. Try: "Create a task to review the Q2 report by Friday."

  Then WAIT for the user's first task request. When it arrives, use the Todo4 MCP tools (e.g., `create_task`) to fulfill it.
- `2` with HTTP 422 → SAY: "Your account has reached the maximum number of connected agents. You can manage them at todo4.io." STOP.
- `2` otherwise → SAY: "Connection failed. Let me try again from the start." Go back to STEP 1.
- `1` → SAY: "I couldn't reach the Todo4 server. Please check your connection and try again." STOP.

Never print `$ACCESS_TOKEN`, the agent token, or the MCP config contents. The `$WEB_LOGIN_URL` is safe to display once (single-use, 5-minute expiry).

---

## Security rules (apply to every step)

- NEVER echo the OTP verification code back to the user. If you must reference it, say "the code you entered."
- NEVER display the access token, refresh token, agent token, or MCP config contents.
- If a script produces unexpected output, summarize the problem in plain English — do not quote raw JSON that may contain secrets.
