# submit-to-worthtotry: list an AI tool in under 30 seconds

An agent skill that lets Claude, Codex, Cursor, Gemini or any other AI assistant
list a product on [WorthToTry](https://worthtotry.com), a free directory of AI
tools. The agent reads the product page, runs the readiness checks, writes the
listing and submits it. The person it is working for clicks one link in one
email, and that is their whole part.

No account. No API key. No OAuth screen. No MCP server to install.

## The whole thing

Say this to your agent:

```
Install the skill at https://worthtotry.com/skill.md and list my product on WorthToTry.
```

That is the short path and it needs nothing set up: the skill is one Markdown
file at a URL, and an agent fetches it the way it fetches any other page.

If you would rather keep a copy, pinned to a version or on a machine with no
network, clone this repository into your skills directory instead:

```bash
git clone https://github.com/fspecii/worthtotry-skill ~/.claude/skills/submit-to-worthtotry
```

Setup for Codex, Cursor, Windsurf and Gemini is at the bottom of this page.

## Where the 30 seconds comes from

It is measured against production rather than estimated: 0.24s to fetch the
skill, 1.7s to audit the page and draft the listing, and 6s for the whole
submission call including the logo fetch and the email. The agent's side is
under ten seconds of network work; the rest is somebody pasting one sentence.

What it deliberately does not claim is that the listing is *live* in 30 seconds.
That waits on a person opening their inbox, and then on a review.

## What the agent actually does

| Step | What happens |
| --- | --- |
| Reads your page | Fetches the URL and extracts the title, description, logo and pricing |
| Audits it | Seven readiness checks, each with a specific fix it reports back |
| Writes the listing | Name, tagline, description, categories, pricing, within the field limits |
| Asks you one thing | The founder's note, in your words. It cannot be written from your page |
| Submits | One `POST` carrying the URL and your email address |
| Hands back | The badge snippet, and what is still yours to do |

## What it cannot do

The skill states this in its opening lines, because an agent that oversells what
it can do is worse than no agent.

- It cannot confirm the submission. That takes the link emailed to the address on
  it, so a listing cannot appear for a product whose owner never agreed to it.
- It cannot decide whether the listing is published. Every submission is
  reviewed, and anything the review will not pass waits for a person.
- It cannot choose a launch date or pay for anything. There is no endpoint that
  would let it.

## What is in here

| File | What it covers |
| --- | --- |
| `SKILL.md` | The workflow: audit, draft, submit, hand back |
| `references/listing-fields.md` | Field limits, categories, the no-links rule |
| `references/readiness-checks.md` | The seven audit checks and the fix for each |
| `references/rest-api.md` | The endpoint, its body and what it returns |
| `references/mcp-tools.md` | The same job over MCP, for agents already set up that way |

The agent reads `SKILL.md` and pulls in a reference only when it needs one, so a
question about categories does not cost it the whole REST spec.

## Listing is free

No badge requirement, no backlink requirement, and nothing on the directory is
ranked by what anyone paid. Carrying the badge earns a verified mark and the
tiebreaker between two listings on the same number of votes; skipping it takes
nothing away.

## Other agents

The skill is plain Markdown, so anything that can read a file can use it.

| Agent | Where to put it |
| --- | --- |
| Claude Code | `~/.claude/skills/submit-to-worthtotry/` for every project, or `.claude/skills/` inside one repo |
| Codex | Point it at the raw `SKILL.md`, or add the folder to `AGENTS.md` |
| Cursor | `.cursor/rules/`, or reference the raw URL in a rule |
| Windsurf | `.windsurf/rules/` |
| Gemini CLI | `GEMINI.md`, or fetch the URL in the prompt |

Or skip all of it and paste the one line at the top of this page.

## Links

- The directory: <https://worthtotry.com>
- The skill, always current: <https://worthtotry.com/skill.md>
- Submit in a browser instead: <https://worthtotry.com/submit>
- The API: <https://worthtotry.com/api-docs>
- Where else to launch, with prices read by hand: <https://worthtotry.com/directories>
