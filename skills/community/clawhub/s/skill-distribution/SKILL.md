---
name: skill-distribution
description: Publish and distribute an agent skill (SKILL.md) so people can find and install it — skills.sh, ClawHub, agentskill.sh, GitHub, the Hermes hub, Claude Code plugin marketplaces and Anthropic's directory, the ChatGPT/Codex plugin directory, Gemini CLI extensions, and paid marketplaces. Use whenever the user has written a skill and asks how to share, publish, upload, list, submit, release, sell, or get installs for it, asks where skills are discovered, asks about the rules or format a registry requires, or wants to turn a skill into a plugin — even if they only name one marketplace.
license: MIT-0
metadata:
  version: "0.1.1"
  verified: "2026-10-10"
---

# Skill distribution

Get a finished skill in front of the people and agents who would use it. There is no single place to upload a skill: there are open registries that index GitHub, registries you push to with a CLI, plugin directories with review, and paid marketplaces. Each has its own rules, and one repository can serve most of them.

This ecosystem changes monthly. Everything here was checked on the date in `metadata.verified`. Before running a publish command or quoting a fee, open the channel's reference file and re-check its linked doc; say so when something could not be confirmed.

## Workflow

1. **Find out what the user wants.** Reach (most installs), a specific audience (Claude users, ChatGPT users, OpenClaw users, their team), or income. This decides the channels. If they have not said, ask once, then default to reach.
2. **Check the skill is publishable.** Run `python scripts/check_skill.py <skill-folder>`. It checks the rules every registry shares and warns about the ones only some enforce. Fix errors before going further; a skill rejected by one registry's validator usually fails others too. Details: `references/checklist.md`.
3. **Make the GitHub repository the source of truth.** Almost every channel reads from a public repo or accepts one, so set this up first even if the user only asked about one marketplace. Layout below.
4. **Publish channel by channel**, in the order of the table. Read only the reference file for the channel you are working on.
5. **Verify each listing** by installing from it on a clean path, not from the local folder.
6. **Report back** with a table: channel, status, link or command, and what is still waiting on review or on the user.

Do not run a publish, submit, or push command without the user's go-ahead for that channel. Publishing is public and several registries cannot fully un-publish. Logins, identity verification, and payment setup are the user's to do; give them the exact step and wait.

## Pick the channels

| Goal | Channel | How it gets listed | Review | Reference |
|---|---|---|---|---|
| Reach, any agent | **GitHub repo** | You push it | None | `references/open-registries.md` |
| Reach, any agent | **skills.sh** | Nothing to submit; appears once people install with `npx skills add owner/repo` | Automated audits | `references/open-registries.md` |
| Reach, any agent | **agentskill.sh** | Submit the repo or a SKILL.md URL at `/submit` | Automated scoring | `references/open-registries.md` |
| OpenClaw / Hermes users | **ClawHub** | `clawhub skill publish <path>` | Automated scan | `references/open-registries.md` |
| Hermes users | **Hermes skills hub** | Publish or tap a GitHub repo | Automated scan | `references/open-registries.md` |
| Claude Code users | **Your own plugin marketplace** | A `marketplace.json` in the repo | None | `references/plugins.md` |
| Claude.ai, Cowork and Claude Code users | **Anthropic's directory** | Developer portal | Human review | `references/plugins.md` |
| One person or a team on claude.ai | **Zip upload** | Customize > Skills | None | `references/plugins.md` |
| ChatGPT and Codex users | **Universal plugin directory** | OpenAI submission portal | Human review | `references/plugins.md` |
| Gemini CLI users | **Gemini CLI extension** | Public repo, picked up by the gallery | None | `references/plugins.md` |
| Income | **Agensi, SkillHQ, MCP Market** | Creator dashboards or CLI | Per marketplace | `references/paid-marketplaces.md` |

A sensible default for "get it out there": GitHub repo, then skills.sh and agentskill.sh (both free and fast), then ClawHub, then wrap the same repo as a Claude Code plugin marketplace. Directories with human review come last because they take days and want a stable version.

Skills versus plugins: a skill is the content; a plugin is a package that carries one or more skills (plus optional commands, connectors and hooks) through a store. Claude, ChatGPT/Codex and Gemini all distribute through their own plugin or extension format, so reaching those stores means wrapping the skill, not rewriting it. The SKILL.md stays the same.

## One repository for every channel

This layout satisfies the skills CLI, agentskill.sh's repo scan, a Claude Code plugin marketplace and an OpenAI plugin at the same time:

```
my-skills/                         # public GitHub repo
├── README.md                      # what it does, install commands per agent
├── LICENSE
├── skills/
│   └── my-skill/                  # folder name must equal the skill's `name`
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
├── plugin.json                    # OpenAI / portable plugin manifest
└── .claude-plugin/
    ├── plugin.json                # Claude Code plugin manifest
    └── marketplace.json           # makes the repo its own marketplace
```

Keep one copy of each skill under `skills/`. Do not maintain per-registry copies; they drift, and registries that hash content will treat them as different skills.

## What helps a skill get found and installed

- **The description does the selling twice.** Registries use it as the search summary and agents use it to decide when to load the skill. Say what it does and when to use it, with the words people actually search.
- **A README with a copy-paste install line for each agent.** Directory pages render it, and it is what gets shared.
- **Cheap to load.** Keep SKILL.md well under 500 lines and move detail into `references/`. Several indexes show context cost and rank on it.
- **Clean on a security scan.** No piped remote scripts, no reading credentials, no instructions that tell the agent to override the user. Flagged skills get hidden or delisted.
- **Versions and a changelog.** Registries that track releases reward maintained skills; bump the version on every published change.
- **Honest requirements.** Declare needed API keys and binaries. A skill that fails on first run earns the one-star review.
- **Installs come from outside the registry.** A demo of the skill doing real work, posted where the audience is, moves more than any listing tweak. Link the install command, not the homepage.

## When something is not covered

New registries appear constantly. For one not listed here, find its submit or publish doc, check three things — what it reads (a repo, an upload, a CLI push), what license it imposes, and whether a listing can be removed — and tell the user before publishing. `references/sources.md` lists the primary docs and what could not be verified.
