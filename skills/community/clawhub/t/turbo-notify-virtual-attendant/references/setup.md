# Setup

Run this once per number, in a conversation with the person setting it up (the configurator). Talk to them in their language. Ask one thing at a time, and keep each message short.

## 1. Check what is needed

1. Call `list_numbers`. If the tool is missing or refused, the Turbo Notify server is not connected or the key lacks permissions. Tell the person to connect it (the guide on the Turbo Notify documentation site, page "MCP server") and to use the API key template **AI agent (MCP)**, which has the scopes `messages:send`, `messages:read`, `contacts:read`, `groups:read`, `numbers:read` and `events:read`. Stop until it works.
2. Run `python3 --version`. It must be 3.9 or newer. If not, see "Without Python" below.
3. Say in one sentence what is about to happen: you will ask a few questions about the business, then answer customers on WhatsApp in a safe way, starting in **assisted mode** (drafts wait for a person to approve).

## 2. Ask

- The business name, as customers know it.
- The language for the people who run it: Portuguese (`pt`) or English (`en`).
- "Is it just you?" If yes, this person will be administrator and attendant too. If not, ask who the administrators are (numbers with area code) and tell them the attendants need no registration: they use the phone or WhatsApp Web of the connected number.
- Which number to use. Show the result of `list_numbers` (alias, number, status) and let them choose. Keep the number's `id` (`num_…`) and its digits. If the list has no connected number (a new account), stop here: a number is paired in the Turbo Notify dashboard, with the phone at hand, and the MCP tools cannot do it. Tell the person to pair one there (the guide "Quickstart" on the Turbo Notify documentation site, step "Connect your main number"), and to come back when it shows as connected.

## 3. Find the organization id

The workspace is named after the organization, which only events carry.

1. Call `list_events` with `limit` 1 and the chosen `number_id`. Save the raw result to a file. If it has an event, read `organization_id` from it.
2. If there is none (a new account), call `send_text` to the connected number itself (`number` = `+` and its digits) with the text "Configurando o atendente virtual" (or "Setting up the virtual attendant" in English), wait a few seconds, and call `list_events` again. Say what you did and why.

## 4. Create the workspace

Choose a folder to keep the data, by default `~/.turbo-notify/attendant`, and tell the person where it is. Then export:

```
export TN_ASSIST_BASE=~/.turbo-notify/attendant
export TN_ASSIST_ORG=org_…
export TN_ASSIST_NUMBER=num_…
```

If the variables do not persist between commands (each shell call may start fresh), pass them as global flags before the subcommand instead: `tn_assist --base <folder> --org org_… --number num_… status`.

and run `tn_assist init --connected <digits> --business "<name>" --lang <pt|en> --harness <claude-code|claude-desktop|codex|antigravity> --admin <digits> --admin-name "<name>"`.

- **If the administrator number is the connected number**, `init` answers with exit code 2 and a `warning`. Read that warning to the person in their language, in your own words but with every idea in it, and ask whether to register it anyway. Only if they say yes, run the same command again with `--confirm-connected`. Their answer is final. If they say no, ask for another number.
- Prime the cursor so that old messages are not answered: `tn_assist cursor --from-page <file with the list_events result of step 3>`.
- To add more administrators: `tn_assist admin add --number <digits> --name "<name>"`.

## 5. Teach the basics

Use the templates in `assets/templates/<lang>/` as an interview guide: company, offers, pricing, frequent questions, policies, tone, hand-off. Ask for each topic in plain words, write what the person says into a file, and store it with:

```
tn_assist kb-write --path pricing.md --visibility public --description "plans and prices" --from-file <file>
```

For every topic ask "is this for customers to read, or only for the team?" Public files may be said to customers. Internal files (margins, supplier terms, staff rules) must be `--visibility internal`. Never publish something the person did not say is for customers. Details: [knowledge.md](knowledge.md).

## 6. Other systems

If the harness has other MCP servers installed (a catalog, a CRM, an agenda), follow [integrations.md](integrations.md) now.

## 7. Privacy and mode

Give the person the privacy notice from [privacy.md](privacy.md). Confirm that the mode is **assisted** (`tn_assist status` shows it) and explain that the assistant prepares answers and a person approves them with `/enviar` (or `/send`) until they switch to automatic (only Claude Code and Codex with the runner: in Claude Desktop, Cowork and Antigravity the command is refused and the mode stays assisted) with `/modo automático` (or `/mode auto`). Recommend at least the first week in assisted mode.

## 8. First run

Ask the person to write "oi" to the number from a phone that is **not** a registered administrator (a friend, a second SIM): an administrator is never treated as a customer, so their "oi" would be read as a command. Then run one cycle ([tick.md](tick.md)). In assisted mode a draft arrives in the chat of the number with itself and to the administrators. Show it and explain `/enviar`.

Then choose how to keep it running, with the file for the harness: [Claude Code](harness-claude-code.md), [Claude Desktop or Cowork](harness-claude-desktop.md), [Codex](harness-codex.md), [Antigravity](harness-antigravity.md). Say plainly what that harness can and cannot do (for example, Claude Desktop cannot run while the app is closed).

## Without Python

The deterministic guarantees (confinement to the workspace, routing by code, the check on what may leave, caps) come from the helper. Without it you are in **manual mode**: follow the same steps with your file tools, keep to the workspace folder, store every message before answering, never include another customer's data, and use assisted mode only. Say this limit to the person before starting, and recommend installing Python 3.9 or newer.
