###### WIP Computer

[![npm](https://img.shields.io/npm/v/@wipcomputer/universal-installer)](https://www.npmjs.com/package/@wipcomputer/universal-installer) [![CLI / TUI](https://img.shields.io/badge/interface-CLI_/_TUI-black)](https://github.com/wipcomputer/wip-universal-installer/blob/main/install.js) [![OpenClaw Skill](https://img.shields.io/badge/interface-OpenClaw_Skill-black)](https://clawhub.ai/parkertoddbrooks/wip-universal-installer) [![Claude Code Skill](https://img.shields.io/badge/interface-Claude_Code_Skill-black)](https://github.com/wipcomputer/wip-universal-installer/blob/main/SKILL.md) [![Universal Interface Spec](https://img.shields.io/badge/Universal_Interface_Spec-black?style=flat&color=black)](https://github.com/wipcomputer/wip-universal-installer/blob/main/SPEC.md)

# Universal Installer

Here's how to build software in 2026.

## The Badges

The chiclets at the top of this README tell you what interfaces this repo ships. Every repo that follows the Universal Interface Spec declares its interfaces the same way.

| Badge | What it means |
|-------|--------------|
| **npm** | Published to npm. Installable via `npm install`. Versioned, dependency-managed, standard distribution. |
| **CLI / TUI** | Ships a command-line interface. Humans run it in a terminal. Agents call it from shell. The most portable interface there is. |
| **OpenClaw Skill** | Registered as a skill on [ClawHub](https://clawhub.ai). OpenClaw agents can discover and use it natively through the gateway. |
| **Claude Code Skill** | Has a `SKILL.md` that teaches Claude Code (and any agent that reads markdown) when to use this tool, what it does, and how to call it. Follows the [Agent Skills Spec](https://agentskills.io/specification). Process in SKILL.md, context in `references/`. |
| **Universal Interface Spec** | Follows the [TECHNICAL.md](TECHNICAL.md) convention. The repo's architecture is documented, the interfaces are declared, and any agent or human can understand the full surface area by reading one file. |

When you see these badges on a WIP repo, you know exactly how to consume it. Human or agent, CLI or plugin, local or remote. That's the point.

## The Problem

Most software is built for humans. GUIs, dashboards, web apps. Humans click buttons, fill forms, read screens.

But the users are changing. AI agents are the new users. They don't click. They call functions. They read instructions. They compose tools. They need a **universal interface** ... multiple ways into the same logic, native to however the consumer works.

Software built for humans doesn't work for agents. And software built only for agents doesn't work for humans. You need both.

`ldm install` gives all your repos the Universal Interface, and teaches your AI how to do it too.

## The Karpathy Argument

Andrej Karpathy put it clearly:

> "I think the app store, the move to mobile, the concept of an app ... is an increasingly outdated concept. What matters are sensors and actuators. Sensors are things that convert physical state into digital state. Actuators are things that convert digital intent into physical change."
>
> "All LLMs care about are tools and the tools fall into this sensor/actuator divide. Software shouldn't be built into apps, but into small bespoke tools. Apps are for people. Tools are for LLMs, and increasingly, LLMs are the ones using software."

[Source](https://x.com/karpathy/status/2024583544157458452)

This is the future of software. Not apps. Tools. Sensors and actuators that agents compose together.

## Install

Open your AI and paste this:

```
Read wip.computer/install/wip-ldm-os.txt

Then explain:
1. What is LDM OS?
2. What does it install on my system?
3. What changes for us? (this AI)
4. What changes across all my AIs?

Check if LDM OS is already installed.

If it is, show me what I have and what's new.

Then ask:
- Do you have questions?
- Want to see a dry run?

If I say yes, run: ldm install --dry-run

Show me exactly what will change. Don't install anything until I say "install".
```

See [SPEC.md](SPEC.md) for the architecture layers, the **eight interfaces** (CLI, Module, MCP local stdio, Remote MCP, OpenClaw Plugin, Skill, Claude Code Hook, Claude Code Plugin), the install spec URL convention, track flags (alpha/beta), and the `agent.txt` distinction. See [TECHNICAL.md](TECHNICAL.md) for sensors/actuators, the interface table, and real examples.

---

## License

```
CLI, module, skills                            MIT    (use anywhere, no restrictions)
Hosted or cloud service use                    AGPL   (network service distribution)
```

AGPL for personal use is free.

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
