# Setting b24 up

These instructions work without a session: `b24 skill show`. `b24 skill install` puts them where Claude Code, Codex,
Gemini CLI and OpenClaw look; `--for hermes` adds Hermes Agent too.

1. **Install:** `npm install -g @wirecat/bitrix24-cli`. It needs Node.js 22.16 or later. Another package, `b24-cli`,
   also installs a `b24`: if the wrong tool answers, call `wcat-b24`, the same program.
2. **The webhook.** The owner makes an inbound webhook in Bitrix24: Developer resources → Common use cases → Other →
   Inbound webhook, with the scopes `crm`, `user_basic` and `department` (and `task` for tasks on deals, `telephony`
   for calls, `disk` and `documentgenerator` for files and documents). `b24 work setup`, in the owner's terminal or in WireCat Desktop, walks them through it. Its address is the password:
   anyone who has it acts as the employee who made it. **Never ask the owner to paste it into the conversation.**
3. **Sign in:** the owner runs `b24 work session start` in their own terminal, which asks for the address hidden and
   checks it against the portal. `work` is the profile, a name the owner picks for this portal. Then
   `b24 work session status --check --json` says whose rights the webhook carries and whether they are an
   administrator. `b24 session list` lists the profiles on this computer.
   Instead of a webhook, a portal may have a local application (Server mode, handler path
   `https://wirecat.dev/webhooks/apps/b24-callback`). The owner then runs
   `b24 work session start --portal <portal> --client-id <id>` and allows it in the browser. It acts as the employee
   who signed in, and every rule that names the webhook's user applies to them. `b24` renews its tokens.
4. **Choose whose deals to copy.** A sync copies only the deals and leads of the users chosen in
   `crm.bitrix24:<portal>.unassigned`, and the clients on them. Nobody is chosen by default, not even the webhook's own
   user: a webhook is often a colleague's. `b24 work users list` shows the ids; the owner runs
   `b24 work config set crm.bitrix24:example.bitrix24.ru.unassigned 12,34` with their portal's host. **Only the owner
   chooses**; an agent's `config set` of `unassigned`, `scope` or `self` is refused. An administrator's webhook may
   choose anyone; anyone else's only themselves, a dismissed user or a user who is not an employee.
5. **Sync:** `b24 work sync`, then `b24 work store status`. The first one may take several runs: each stops before
   its deadline, says `complete: false`, and the next goes on.
6. **Keep it fresh**, only if the owner asks: `b24 work schedule command crm --every 1h -- sync` installs a timer on
   this computer. Not over MCP.
7. **Permissions** before an agent gets the CRM: [mcp.md](mcp.md) and `b24 guide safe-agent-writes`.

## Traps

- **`B24_CONFIG_DIR` and `B24_STATE_DIR` move the folders**, and a sign-in made with them goes to a temporary keyring
  entry that `session end` removes. With them, a profile may answer "not signed in" although the owner is, and an
  expired local-application sign-in is not renewed: renew it in a run without moved folders. `b24 work config show`
  and `b24 doctor` say whether they are set.
- **`B24_READ_ONLY=1` refuses every write**, whatever the permissions say. An agent `schedule agent` starts runs
  with it.
- **Before you report a bug**, compare `b24 -V` with `npm view @wirecat/bitrix24-cli version`; an older install may
  lack the fix. `b24 upgrade --check` says the same.

Guides for people: [usage](https://github.com/WireCatLabs/bitrix24-cli/blob/main/docs/usage.md),
[permissions](https://github.com/WireCatLabs/bitrix24-cli/blob/main/docs/permissions.md),
[MCP](https://github.com/WireCatLabs/bitrix24-cli/blob/main/docs/mcp.md).
