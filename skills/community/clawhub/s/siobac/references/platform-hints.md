# Platform hints — per-host first-run notes

Some agent platforms have quirks that change how Siobac should be set up or run. **On your
first run, identify your host and read its note below** — it tells you the one extra thing to
do (or avoid) on that platform. If your host isn't listed, the defaults are fine.

## How to TURN ON a platform note (the trigger)

The only trigger is the **`SIOBAC_PLATFORM`** environment variable. These hosts do NOT set it
for you, so **YOU (the agent) must set it** — you generally know your own host (from your system
context) or the owner tells you. Set it to your host id and **pass it on EVERY siobac command
this session** (these hosts give you no persistent place to save it):

```
SIOBAC_PLATFORM=doubao     node …/cli.js <command>
SIOBAC_PLATFORM=qclaw      node …/cli.js <command>
SIOBAC_PLATFORM=workbuddy  node …/cli.js <command>
```

- **qclaw / workbuddy:** set it on every command so the **pre-login model check** fires (it runs
  on `login`, each time).
- **doubao:** the essential per-run env var is **`SIOBAC_TOKEN`** (your portable login — see below);
  pass `SIOBAC_PLATFORM=doubao` alongside it to keep the portable reminder visible.

When set, `doctor`/`login` echo the matching note in `platform_hint`, and the right cue fires at
the right moment. (No env var set → defaults; the skill still flags the wiped-FS *symptom* if it
sees one. You can always just match your host to the list yourself.)

---

## doubao — ephemeral workspace (sandbox recycled on idle)

**Symptom:** you log in and it works fine for a while — then you leave the chat for a few hours,
come back **in the same session**, and suddenly it reports "not authenticated" / asks you to log
in again. It is NOT every run, and it is NOT a token expiring (your tokens are still valid for
days). Doubao keeps the sandbox **warm while you're active** but **recycles it on idle**: after the
session sits a few hours, BOTH the filesystem (`~/.siobac/auth.json`) AND the process environment
(`SIOBAC_TOKEN`) are wiped, even though the conversation continues. The only thing that survives a
recycle is **your conversation memory** — so whatever you set "once at the start" is gone, and the
skill, seeing no credentials, falls back to asking for a re-login.

**Fix — portable login (a non-rotating token you keep in durable memory).** Handle this SILENTLY:
never explain tokens to the owner and never show them a command to run — they only need to hear
that login succeeded.
1. Log in once normally (`login` → `login --finish`). On doubao, `login` **AUTO-mints** the portable
   token and returns it as the **`portable_token`** field (plus an agent-only `portable_login` note)
   — no separate command needed. (Fallback only if that field is absent: run **`issue-portable-login`**.)
2. Memorize the **`portable_token`** value (NOT the short-lived access token).
3. **Save that token in your durable conversation memory** (it does NOT change).
4. **REHYDRATE BEFORE EVERY RUN — not once per session.** At the very start of *every* turn, BEFORE
   any siobac command, re-establish the credential from your memorized token: set the
   **`SIOBAC_TOKEN`** environment variable (or, if you can only write files, re-write
   `~/.siobac/auth.json` with `{"refreshToken":"<token>","tokenType":"Bearer","expiresAt":"1970-01-01T00:00:00Z"}`).
   This is **idempotent and cheap** (the 7-day token never changes), and it is the ONLY thing that
   survives an idle recycle. Do not assume "I already set it this session" — you cannot tell whether
   the sandbox was recycled since your last turn, so always re-inject.
5. The skill exchanges it for a fresh access token in-memory each run — **no re-login**.
   Re-run `issue-portable-login` every ~7 days; `revoke-portable` kills it if leaked.

> If you get "not authenticated" after an idle gap, the fix is to **re-inject your memorized
> portable token and retry** — do NOT bounce the owner to a login screen. The token is still valid.

**Security:** the portable token is a bearer credential — treat it like a password. NEVER show
it to anyone the agent talks to; only the owner/host environment should hold it.

---

## qclaw / workbuddy — suggest the best model (Deepseek-V4-Pro)

These platforms let the owner choose the underlying LLM, and Siobac runs noticeably better on
**Deepseek-V4-Pro**. This is a **SUGGESTION, never a requirement** — whatever they pick, carry on.

**This is its OWN first step, BEFORE the login link — never both at once.** When you run `login`
on these platforms the skill returns `status: "model_check_first"` and mints NO login link yet.
Handle the model suggestion first, THEN run **`login --model-checked`** to get the actual login
link. (Showing the suggestion and the login link together buried the login — so they are now
strictly sequential: model check → then login.)

Check which model YOU are running:
- **Already on Deepseek-V4-Pro (condition no longer triggers)** → SKIP the suggestion silently;
  immediately run `login --model-checked` to continue. Don't mention it.
- **NOT on Deepseek-V4-Pro** → offer the suggestion ONCE (don't nag), with exactly two options.
  Do NOT name the platform in the message — keep it simple:
  > Quick tip — I run best on **Deepseek-V4-Pro**; switching gives you a smoother experience.
  > Totally optional.
  > 1. ✅ I've already switched · 2. 👍 Keep the current model
  After the user responds (either choice — option 1 = they switched, option 2 = stay as-is), run
  `login --model-checked` to continue to the login. Do NOT block anything on it, and don't raise it
  again this session.

**How the platform/model is known:** the host (or owner) can set `SIOBAC_PLATFORM=qclaw` /
`workbuddy` (then `doctor`'s `platform_hint` flags this note); and YOU (the agent) know which model
you're running, so you can self-assess without any extra tooling.

---

## (template for adding a platform)

## <platform-id> — <one-line situation>
**Symptom:** <what the agent/owner observes>
**Fix:** <the steps, in plain words>
**Security/Caveats:** <anything to be careful of>
