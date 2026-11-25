# Setting amo up

These instructions work without a session: `amo skill show`. `amo skill install` puts them where Claude Code, Codex,
Gemini CLI and OpenClaw look; `--for hermes` adds Hermes Agent too.

1. **Install:** `npm install -g @wirecat/amo-cli`. It needs Node.js 22.16 or a later 22.x, or 24 or later.
2. **The integration.** An account administrator makes a private (external) integration in amoCRM (амоМаркет → ⋯ →
   «Создать интеграцию») or Kommo (Settings → Integrations → Create integration), with access to the account's data.
   Its **long-lived token** (the «Ключи» tab, Kommo: Keys and scopes) is the password: anyone who has it acts as the
   administrator who made it. **Never ask the owner to paste it into the conversation.** `amo work setup`, in the
   owner's terminal, walks them through it. An owner who is not an administrator (no амоМаркет in their menu) asks an
   administrator for that token; the setup's "not an administrator" answer shows the request to send.
3. **Sign in:** the owner runs `amo work session start --host https://<subdomain>.amocrm.ru` in their own terminal,
   which asks for the token hidden, checks it against the account and keeps it with the address. `work` is the
   profile, a name the owner picks for this account. Then `amo work session status --check --json` says which account
   and user the token acts as. `amo session list` lists the profiles on this computer.
   - With `--one-click` an administrator of an amoCRM account (`*.amocrm.ru`, not Kommo) signs in with one click
     instead: amoCRM's button on connect.wirecat.dev creates a WireCat integration in the account, its secret key
     passes through connect.wirecat.dev once, and `amo` renews the sign-in. Only the owner clicks «Разрешить» in the
     browser; an agent never runs it unasked.
   - With `--client-id <integration id>` the owner signs in through the integration in the browser instead, and acts
     with their own rights. `amo` renews those tokens. amoCRM offers only accounts where the person is an
     administrator, so this way is for administrators.
   - `AMO_TOKEN` with `AMO_HOST` (the account's address) signs in without a saved sign-in, for a script. `AMO_TOKEN`
     alone is refused (`account.host-missing`).
4. **Choose whose deals to copy.** A sync copies the deals of the sign-in's own user and the clients on them. An
   administrator may choose other users in `crm.amocrm:<address>.unassigned`, with their own id among them, since the
   list replaces it: `amo work users list` shows the ids, and the owner runs
   `amo work config set crm.amocrm:example.amocrm.ru.unassigned 7001,7002` with their account's address. Anyone else
   may choose only themselves. **Only the owner chooses**; an agent's `config set` of `unassigned`, `scope`,
   `stage-tasks` or `activities` is refused. `scope` is `mine` by default, and `sync` refuses `all`.
5. **Sync:** `amo work sync`, then `amo work store status`. The first one may take several runs: each stops before
   its deadline, says `complete: false`, and the next goes on.
6. **Keep it fresh**, only if the owner asks: `amo work schedule command crm --every 1h -- sync` installs a timer on
   this computer. A morning digest:
   `amo work schedule command crm-digest --at 08:30 -- changes list --format report`.
7. **Permissions** before an agent gets the CRM: [mcp.md](mcp.md) and `amo guide safe-agent-writes`.

## Two settings only the owner sets

- **`crm.amocrm:<address>.activities`** is off by default. Turned `on`, each sync also copies the tasks, comments and
  calls on the kept deals and their clients, from the last 90 days ([reading.md](reading.md)).
- **`crm.amocrm:<address>.stage-tasks`** opens a task on this computer, beside the owner's other WireCat tasks, for
  each deal that moves into a stage it names. The sync that brings the move opens it, once per move: a dismissed task
  does not come back, and the next entry into the same stage opens a new one. A stage is named by its id
  (`amo work stages list --json` prints `external_id`), and the value is JSON:
  `{"<stage id>": {"title": "Send the closing papers", "due_days": 2}}`. amoCRM's won stage is `142` in every
  pipeline, so a rule on `142` fires on a win in any pipeline. `amo` reads the account's stage history, so a stage a
  deal passed through between two syncs still opens its task. Moves before the setting was first set open none.

## Traps

- **`AMO_CONFIG_DIR` and `AMO_STATE_DIR` move the folders**, and a sign-in made with them goes to a temporary keyring
  entry that `session end` removes. With them, a profile may answer "not signed in" although the owner is.
  `amo work config show` and `amo doctor` say whether they are set.
- **`AMO_READ_ONLY=1` refuses every write**, whatever the permissions say. An agent `schedule agent` starts runs
  with it.
- **A token has an end date** the administrator picked. After it, or after a revoke, every command answers
  `session.expired` (exit `4`): the owner makes a new token and runs `session start` again.
- **Before you report a bug**, compare `amo -V` with `npm view @wirecat/amo-cli version`; an older install may lack
  the fix. `amo upgrade --check` says the same.

Guides for people: [install and connect](https://github.com/WireCatLabs/amo-cli/blob/main/docs/installation.md),
[use it](https://github.com/WireCatLabs/amo-cli/blob/main/docs/usage.md),
[settings](https://github.com/WireCatLabs/amo-cli/blob/main/docs/configuration.md).
