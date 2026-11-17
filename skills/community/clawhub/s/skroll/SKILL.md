---
name: skroll
description: Write, publish, version and export Skroll decks from the terminal. YOU write the deck (one React/TSX module); Skroll compiles, stores and publishes it. Use when the user wants a Skroll presentation, pitch deck, slides, or PDF/PPTX export. Requires the Skroll CLI (`npx @skrollai/cli`).
license: MIT
compatibility: Requires Node.js 22+ and network access to skrollai.com
metadata:
  author: hamburgerlabs
  homepage: https://skrollai.com
---

# Skroll

ALWAYS READ THIS FIRST. THIS IS ESSENTIAL.

Skroll is a browser-canvas presentation tool. This skill drives it through the official CLI, which uses the same OAuth login as the MCP server.

**You are the designer.** Skroll does not generate the deck for you: you write one React/TSX module and Skroll compiles it, versions it and publishes it.

Run `npx @skrollai/cli instructions` before you write anything. It prints the brief the Skroll app's own agent designs from. Do not skip it. Do not write a deck from memory of what slides usually look like. That brief is the difference between a deck someone is proud to present and a web page in a deck's clothing.

## Setup

Needs Node.js 22+.

**If you cannot open a browser** (headless agent, CI, container), do not run `login`. It
waits five minutes for a browser callback and then times out. Ask the user for an API key
from https://skrollai.com/app/settings/integrations and export it:

```bash
export SKROLL_API_KEY=sk_…      # or SKROLL_TOKEN=<OAuth access token>
```

**If a browser is available**, log in once (PKCE, no API key needed), then confirm:

```bash
npx @skrollai/cli login
npx @skrollai/cli whoami
```

A first-time user is signed up and given an organization automatically during `login`;
there is nothing to set up in the web app first.

Default origin is `https://skrollai.com`. Override with `--origin` or `SKROLL_ORIGIN` for local
or self-hosted instances. Log in once per origin, since a stored credential is only ever sent
to the host that issued it. `--token` / `SKROLL_TOKEN` works against any origin.

## Commands

The CLI maps 1:1 to the Skroll MCP tools (plus `download_export`, which writes a file). Run `npx @skrollai/cli help` for flags.

| Task | Command |
| --- | --- |
| **ALWAYS READ THIS FIRST (essential)** | `npx @skrollai/cli instructions` |
| List decks | `npx @skrollai/cli list_decks` (add `--scope org` for the whole organization; default is your own) |
| Create a blank deck | `npx @skrollai/cli create_deck --title "Q3 review"` (add `--brand-id <id>` to style it) |
| Start from a template or any deck | `npx @skrollai/cli create_deck --title "Q3 board" --from-deck-id <deckId>` |
| Create a template | `npx @skrollai/cli create_deck --title "Board pack" --kind template --description "Monthly board update"` |
| Save the deck you wrote | `npx @skrollai/cli set_deck_content --id <deckId> --source @deck.tsx --tokens-css @tokens.css` |
| Inspect a deck | `npx @skrollai/cli get_deck --id <deckId>` (returns the current module, so you can edit and save it back) |
| Patch title or visibility | `npx @skrollai/cli update_deck --id <deckId> --title "New title"` |
| Delete a deck | `npx @skrollai/cli delete_deck --id <deckId>` |
| Versions | `list_deck_versions`, `get_deck_version`, `revert_deck_version` |
| Export PDF / PPTX | `create_export --id <deckId> --format pdf` then `get_export --id <exportId>` |
| Download the file | `download_export --id <exportId> --out ./deck.pdf` |
| Brands | `list_brands`, `get_brand`, `delete_brand` |
| List templates | `npx @skrollai/cli list_decks --kind template` |
| Sign out | `npx @skrollai/cli logout` |

Commands print the raw API payload, except `instructions`, which prints the brief as plain text and opens with `ALWAYS READ THIS FIRST`. Prefix a flag value with `@` to read it from a file, which is how you pass a module you just wrote.

Editing means rewriting: `get_deck` returns the current module, you change it, and `set_deck_content` saves the whole thing as a new version. There is no partial write.

`create_export` is asynchronous: poll `get_export` until status is `completed`, then `download_export`.

## Templates

A template is an **ordinary skroll** that the organization starts new work from. It has
versions, it opens in the same workspace, it edits through the same chat and it exports
the same way. The only difference is `kind: "template"`, a description saying what it is
for, and the fact that it is offered as a starting point. There is no separate template
API and nothing to convert.

Find one, then build on it:

```bash
npx @skrollai/cli list_decks --kind template          # read the descriptions, pick one
npx @skrollai/cli create_deck --title "Q3 board" --from-deck-id <templateId>
npx @skrollai/cli set_deck_content --id <deckId> --source @deck.tsx
```

`--from-deck-id` takes any skroll you can read, so a deck nobody has templated works too.
It is a starting point, not a copy: the first version is written fresh into that design.
This API only authors slides, so a webpage starting point is refused. Brand comes from
it unless you pass `--brand-id`.

Create a template directly rather than making a skroll and converting it:

```bash
npx @skrollai/cli create_deck --title "Monthly board update" --kind template \
  --description "Numbers first, one slide per business unit"
npx @skrollai/cli set_deck_content --id <deckId> --source @template.tsx
```

Write the description for whoever picks it next: say what it is FOR, not what it looks
like. `update_deck --kind template` promotes a skroll the team already likes, and
`--kind deck` demotes it. Prefer `update_deck --archived true` over deleting: skrolls
built from a retired template still name it.

**Write it as a template, not as a deck.** Whoever starts from one keeps the design and
replaces the words, so anything specific to a company or a quarter is the first thing
they delete. Aim for around five slides, one of each layout worth reusing (title, section
divider, text beside an image, one numbers slide, a closing), with visibly placeholder
copy and no invented logos, customers, metrics or team members. Skroll finds photography
itself and credits the photographer; do not invent image URLs, which do not resolve.

```bash
npx @skrollai/cli set_deck_content --id <deckId> --source @template.tsx
```

## Errors worth handling

Every failure is JSON: `{"error":{"code":…,"message":…}}`. Three are worth reacting to
rather than retrying:

- **402 `payment_required`**: the organization has used its free allowance (10 skrolls,
  100 edits). Retrying will never succeed. Tell the user, and point them at
  https://skrollai.com/app/settings/billing.
- **422 `invalid_input`** on `set_deck_content`: the module did not compile, and the message is the
  compiler's. Nothing was saved. Fix the module and send it again; this round trip is normal.
- **429 `rate_limited`**: back off for the `retryAfterSeconds` in the response. `create_export` has a
  budget of 10 per minute; everything else is 120 per minute.
- **401 `unauthorized`**: the session expired or was revoked. Run `login` again, or check
  `SKROLL_API_KEY`.

## Sharing

Public viewer URLs look like `https://skrollai.com/d/f4zqohxo7d`. After `update_deck --visibility public`, share the `publicUrl` field from the JSON. `get_deck` and `list_decks` return the same field when the skroll is public. Never invent a share link from the deck id, title, or API path.

## Docs

- Product: https://skrollai.com
- CLI: https://skrollai.com/developers/cli
- MCP (same tools, OAuth in the client): https://skrollai.com/developers/mcp
- REST: https://skrollai.com/developers
- skills.sh: `npx skills add hamburgerlabs/skroll`
