# Tavily Skill Onboarding Flow (for OpenClaw Agents)

> Goal: help beginners complete installation + API key setup + verification with minimal confusion.

## Language policy

- Default to the user's language (prefer Chinese if user context is Chinese).
- Keep instructions short, step-by-step, and confirm completion at each step.

## Fixed flow

1. Confirm install success and paths silently
   - `~/.openclaw/workspace/skills/tavily-search`
   - script exists: `scripts/tavily_search.mjs`
   - do not print full path-by-path checklist unless user asks
2. Ask user whether to start guided key setup now, in the user's preferred language.
3. Guide user to open https://tavily.com and sign in/sign up.
4. Guide user to create/copy API key.
5. Guide user to set `TAVILY_API_KEY` in `~/.openclaw/.env`.
   - First offer the easiest “open with Notepad/TextEdit” path (no shell knowledge required).
   - Then offer VS Code / terminal alternatives only as secondary options.
   - Prefer manual local edit (safer).
   - If user asks for convenience, agent can write it.
6. Ask user to confirm: "I configured it".
7. Ask whether to run a quick test now.
8. If test fails, proactively troubleshoot:
   - Missing key / malformed key
   - Proxy/network issue
   - Timeout / rate-limit (429)
   - Invalid endpoint or parameter mismatch

## Suggested verification command

```bash
node scripts/tavily_search.mjs search --query "OpenClaw multi-agent" --max-results 3 --format brave
```

Add `--proxy http://127.0.0.1:7890` when needed.
