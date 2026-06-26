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
| **Claude Code Skill** | Has a `SKILL.md` that teaches Claude Code (and any agent that reads markdown) when to use this tool, what it does, and how to call it. The agent reads the file and learns the capability. |
| **Universal Interface Spec** | Follows the [SPEC.md](SPEC.md) convention. The repo's architecture is documented, the interfaces are declared, and any agent or human can understand the full surface area by reading one file. |

When you see these badges on a WIP repo, you know exactly how to consume it. Human or agent, CLI or plugin, local or remote. That's the point.

## The Problem

Most software is built for humans. GUIs, dashboards, web apps. Humans click buttons, fill forms, read screens.

But the users are changing. AI agents are the new users. They don't click. They call functions. They read instructions. They compose tools. They need a **universal interface** ... multiple ways into the same logic, native to however the consumer works.

Software built for humans doesn't work for agents. And software built only for agents doesn't work for humans. You need both.

`wip-universal-installer` gives all your repos the Universal Interface, and teaches your AI how to do it too.

## The Karpathy Argument

Andrej Karpathy put it clearly:

> "I think the app store, the move to mobile, the concept of an app ... is an increasingly outdated concept. What matters are sensors and actuators. Sensors are things that convert physical state into digital state. Actuators are things that convert digital intent into physical change."
>
> "All LLMs care about are tools and the tools fall into this sensor/actuator divide. Software shouldn't be built into apps, but into small bespoke tools. Apps are for people. Tools are for LLMs, and increasingly, LLMs are the ones using software."

[Source](https://x.com/karpathy/status/2024583544157458452)

This is the future of software. Not apps. Tools. Sensors and actuators that agents compose together.

## Install

Open your AI coding tool and say:

```
Read the SPEC.md and SKILL.md at github.com/wipcomputer/wip-universal-installer.
Then explain to me:
1. What is this tool?
2. What does it do?
3. What would it change or fix in our current system?

Then ask me:
- Do you have more questions?
- Do you want to integrate it into our system?
- Do you want to clone it (use as-is) or fork it (so you can contribute back if you find bugs)?
```

Your agent will read the repo, explain the tool, and walk you through integration interactively.

Also see **[wip-release](https://github.com/wipcomputer/wip-release)** ... one-command release pipeline for agent-native software.

Also see **[wip-file-guard](https://github.com/wipcomputer/wip-file-guard)** ... the lock for the repo. Blocks AI agents from overwriting your critical files.

See [REFERENCE.md](REFERENCE.md) for sensors/actuators, the interface table, how to build it, the installer, and real examples.

---

## License

```
CLI, module, skills                            MIT    (use anywhere, no restrictions)
Hosted or cloud service use                    AGPL   (network service distribution)
```

AGPL for personal use is free.

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
