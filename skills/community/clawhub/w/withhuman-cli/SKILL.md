---
name: withhuman-cli
description: Connect coding agents and other agent runtimes to withHuman with the withhuman CLI so their tool calls wait for human approval. Covers installing the CLI, guided onboarding, connecting a runtime to an existing agent, checking the connection, refreshing the tool catalogue, upgrading, and removing the adapter. Use for Claude Code, Codex, OpenClaw, Pi, Hermes and DeepSeek on macOS or Linux, hosted or self-hosted. Trigger keywords - withhuman, withHuman CLI, install withhuman, connect agent to withhuman, withhuman onboard, withhuman agent install, agent eject, refresh-tools, approval hook, calls not gated, human approval for tool calls.
---

# withHuman CLI

The `withhuman` CLI connects an agent runtime on this machine to a
withHuman organization. After it is installed, every tool call the runtime
makes is sent to withHuman first. The organization's approval pipeline
decides whether the call runs at once, is denied, or waits for a person to
approve it.

Each installation connects one runtime (`claude-code`, `codex`, `openclaw`,
`pi`, `hermes` or `deepseek`) as one **instance** of an **agent** in the
organization. The CLI runs on macOS and Linux, Intel and ARM.

## Ground rules

- **The person runs the interactive steps.** Installation can ask for an
  administrator password, and connecting opens a browser where the person
  signs in and confirms the organization and agent. Give them the command
  to run, or run it only when they can answer the prompts.
- **Never read, print or copy credentials.** Saved connections live in the
  CLI's configuration directory (`~/Library/Application Support/withhuman`
  on macOS, `~/.config/withhuman` on Linux, or `$WITHHUMAN_CONFIG_DIR`).
  Don't open them.
- **Never remove or bypass the adapter on your own initiative.** Run
  `withhuman agent eject` or edit the runtime's hook settings only when the
  person asks. If you are the agent being gated, a call that waits or is
  denied is the system working, not a fault to route around.
- **Restart the runtime when told to.** A runtime loads its hooks at start,
  so the CLI's printed restart or consent steps must be followed before a
  test means anything.

## Which server

Hosted withHuman is `https://app.withhuman.ai` and is the default. A
self-hosted deployment has its own origin, for example
`https://approvals.example.com`: pass it with `--url` or set
`WITHHUMAN_URL`. Give the origin only, without `/api/aap`. Ask the person
which one they use if it is not clear.

## First-time setup (new organization)

Guided setup lives in the web app at `<origin>/welcome` (hosted:
<https://app.withhuman.ai/welcome>). The page shows a command with a
one-time setup code, so the person must copy it from their own page:

```sh
curl -fsSL https://downloads.withhuman.ai/install.sh | sh -s -- onboard --url https://app.withhuman.ai --code <code>
```

Leave the command running while the person finishes the browser steps
(choose agents, notification channels, which tools wait, a test request).
You cannot make up the code; if it expired, the person reloads the page for
a new one.

## Connect a runtime to an existing organization

Install the CLI (skip if `withhuman version` already works):

```sh
curl -fsSL https://downloads.withhuman.ai/install.sh | sh
```

Then connect a runtime:

```sh
withhuman agent install claude-code
withhuman agent install codex --agent coding-agents --instance codex-laptop
withhuman agent install codex --url https://approvals.example.com
```

- Omit the runtime to pick from the ones found on this machine. Without a
  terminal, name it.
- `--agent <slug>` joins an agent that already exists in the organization;
  it never creates one. Without it, the person chooses or creates the agent
  in the browser.
- `--instance <name>` names this machine's instance. The default is the
  hostname plus a short suffix.
- The CLI opens the browser. If it cannot, the person visits the printed
  address and enters the code. Codes last ten minutes.
- Running install again with a working connection reuses it without another
  browser step.

On hosted withHuman the install also registers the withHuman MCP Gateway
with the runtime as an MCP server named `withhuman-gateway`, so the agent
can use tools granted to it there. It is not the withHuman MCP server that
manages rules (see the `withhuman-pipelines` skill).

The app's **Agents** page also has **New instance**, which prints the same
command with the agent and origin filled in.

## Check it works

```sh
withhuman agent discover
```

Each runtime found reports `adapter installed`, `incomplete` (follow the
restart or repair steps, then rerun install) or `not installed`.

Then trigger a call that the organization's rules send to a person, for
example a shell command if shell commands wait. The runtime pauses, the
request appears in the app's **Review queue** and the person's notification
channels, and the call runs only after they approve it. If every call runs
straight through, the rules may approve it automatically: check the
approval pipeline (see the `withhuman-pipelines` skill) before assuming
the hook is broken.

## Refresh the tool catalogue

The organization builds rules from the tools each instance reports. After
adding or changing MCP servers in the runtime, run this from the project
directory where the runtime uses them:

```sh
withhuman agent refresh-tools claude-code --agent coding-agents
```

It reports successful and failed sources separately. A failed source does
not undo the installation; fix that server's connection and run it again.

## Update and remove

```sh
withhuman upgrade
withhuman agent install <runtime>
withhuman agent eject <runtime>
```

- `upgrade` replaces the CLI with the latest release and keeps connections.
  Rerun `agent install` afterwards to refresh a runtime's adapter files.
- `agent eject` removes the hook, the gateway's MCP entry and the saved
  connection for that runtime. It does not revoke the instance in
  withHuman: tell the person to revoke it under the agent's **Instances**
  tab if it will not be used again.

## Troubleshooting

| Symptom | What to do |
| --- | --- |
| `withhuman: command not found` after install | The installer used `~/.local/bin`; add it to `PATH` or open a new shell. |
| The runtime was not found | Install the runtime first, or name it: `withhuman agent install claude-code`. |
| Browser code expired | Run the same command again for a new code. |
| `--agent` refused | The slug must exist in the organization the person signs in to, and they need permission to connect it. Check the slug on the **Agents** page. |
| Adapter `incomplete` | Follow the printed restart, consent or repair steps, restart the runtime, rerun `withhuman agent install <runtime>`. |
| Calls are not held | Restart the runtime, check `withhuman agent discover`, then check the pipeline: an `approve` block may be deciding them. |
| Credential expired or revoked | Run `withhuman agent install <runtime>` again to reconnect. |
| Every call denied because the provider refused the credential | The agent was archived or disabled, or the credential revoked. Enable or restore the agent and reconnect, or, if the person asks, run `withhuman agent eject <runtime>` to stop gating this runtime. |
| A call waited and then was refused as expired | Nobody decided in time. Tell the person; don't retry it on your own. |

User guides: <https://withhuman.ai/docs/getting-started/quickstart.md> and
<https://withhuman.ai/docs/web-app/agents.md>.
