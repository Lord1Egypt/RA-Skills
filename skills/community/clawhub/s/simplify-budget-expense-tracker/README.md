# Simplify Budget Skill

`simplify-budget` is an OpenClaw skill package for running a personal budget tracker on top of a specific Google Sheets template.

OpenClaw is the messaging/tool host. The active OpenClaw conversation model handles orchestration natively.

It handles:
- expenses: log, find, update, delete
- income: log, find, update, delete
- recurring items: create, inspect, update, delete
- recurring questions such as `what is due this month`
- FX conversion into the tracker currency
- receipt-based expense logging
- safe category confirmation with learned aliases over time

## What This Ships

This skill package contains:
- [SKILL.md](./SKILL.md): skill instructions
- [SETUP.md](./SETUP.md): end-to-end installation
- `commands/`: bundled command wrappers and dispatcher for OpenClaw routing
- `scripts/`: the actual shell scripts used by the skill
- `data/learned_category_aliases.json`: confirmed category hints learned from real usage

This package is for skill installation. The plugin package is a separate deliverable.

## Orchestration

- The active OpenClaw conversation model handles intent routing, confirmations, and conversation state natively
- OpenClaw owns the message/tool surface and runs the live sheet scripts
- the live sheet remains the source of truth for reads, writes, edits, deletes, and verification
- budget chat flows should not rely on long conversation history

## Required Template

This skill only works with the Simplify Budget sheet template, or a direct copy of it:
- [Simplify Budget Template](https://docs.google.com/spreadsheets/d/1fA8lHlDC8bZKVHSWSGEGkXHNmVylqF0Ef2imI_2jkZ8/edit?gid=524897973#gid=524897973)

If the sheet layout is changed, the scripts will break.

Expected tabs:
- `Expenses`
- `Income`
- `Recurring`
- `Dontedit`

Expected layout assumptions:
- `Expenses` ledger starts at row `5`
- `Income` ledger starts at row `5`
- `Recurring` ledger starts at row `6`
- active categories live in `Dontedit!L10:O39`
- expense and recurring expense categories use `=zategory<stableId>`
- recurring income uses literal `Income 💵`

## Setup

Minimum requirements:
- a copy of the template
- a Google service account JSON key
- the copied sheet shared with that service account
- `GOOGLE_SA_FILE`
- `SPREADSHEET_ID`
- `TRACKER_CURRENCY`

Optional:
- `TRACKER_CURRENCY_SYMBOL`

Install summary:
1. Copy the Google Sheet template.
2. Create your own Google service account JSON key.
3. Share the copied sheet with the service account email.
4. Optionally use [simplifybudget.com](https://simplifybudget.com/) as the browser UI for the same sheet.
5. Install this skill under your chosen OpenClaw home.
6. Use the bundled command wrappers from that installation.
7. Set the required environment variables.
8. Restart OpenClaw.

Full instructions are in [SETUP.md](./SETUP.md).

## Behavior Notes

- New expenses should go through natural-language `log.sh`.
- If the user names a category explicitly, the skill uses it directly.
- If the parser already knows the item, it suggests that category.
- If the parser does not know the item, the LLM suggests a category and asks for confirmation before writing.
- Once the user confirms, the skill can learn that alias for future suggestions.
- The default account is `Revolut` unless the user says otherwise.

## Example Prompts

Expenses:
- `i bought coffee for 5 euro`
- `i bought the pencil for 10 euro under business category`
- `change that coffee to 4 euro`
- `delete that coffee expense`

Income:
- `log income of 100 euro today named test income`
- `change that income account to Revolut`

Recurring:
- `add a monthly test subscription for 10 euro in simplify budget`
- `when is capcut due`

Receipts:
- `log this receipt`
- `add this grocery receipt to simplify budget`

## For Agents

Agent-specific behavior lives in [AGENTS.md](./AGENTS.md).
