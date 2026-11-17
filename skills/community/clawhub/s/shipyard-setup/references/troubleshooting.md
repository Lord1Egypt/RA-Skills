# Troubleshooting setup

Start with `node "${CLAUDE_PLUGIN_ROOT}/scripts/setup-status.mjs"` and `check-tools.mjs`. Fix one thing at a time and re-run the check.

| What they see | What it means and what to do |
|---|---|
| `node` or `npx` not found after installing Node | The terminal started before the install. Close it, open a new one, run `node --version`. Needs 20 or newer |
| `node` older than 20 | Install the current LTS from nodejs.org |
| `gh: command not found` | Install the GitHub tool (see accounts.md step 1), then reopen the terminal |
| `gh auth status` says not logged in | Run `gh auth login --web` again. The code expires after a few minutes |
| `git push` asks for a password | Run `gh auth setup-git` so git uses the GitHub login |
| Vercel login page never finishes | Close it, run `npx --yes vercel@64.3.1 login` again, pick "Continue with GitHub" |
| `vercel whoami` says no credentials | Login did not finish. Run login again |
| `secrets-check` says the Supabase token is missing | Open the keys file again with `secrets-init.mjs`. The line must be `SUPABASE_ACCESS_TOKEN=sbp_...` with no spaces, quotes or line breaks. Save the file |
| Token looks right but `--live` fails with 401 | The token was revoked or copied incompletely. Generate a new one and replace the whole line |
| Keys file opened in the wrong program | Open `~/.shipyard/secrets.env` (Windows: `%USERPROFILE%\.shipyard\secrets.env`) with any text editor |
| Playwright download fails | Check the internet connection and run `npx playwright install chromium` again. Phone-size checks are skipped until it works; apps still build |
| They pasted a key in the chat by mistake | Tell them to revoke that key in the provider's dashboard and make a new one, then paste it into the keys file only |
| Windows: script cannot run | Use the terminal Claude Code runs in. Do not run Shipyard scripts from an old Command Prompt that lacks Node |
| Usage limit reached mid-setup | Nothing is lost. Run `/shipyard:setup` later; it continues at the saved step |
| Not sure what is saved | `node "${CLAUDE_PLUGIN_ROOT}/scripts/profile.mjs" show` (it holds no secrets) |

If none of these fit, ask the student to describe what they see, quote the exact error text in your answer, and suggest opening an issue at github.com/philipposk/shipyard with that text (never with any key).
