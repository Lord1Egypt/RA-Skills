###### WIP Computer

[![Module](https://img.shields.io/badge/interface-Module-black)](#) [![MCP Server](https://img.shields.io/badge/interface-MCP_Server-black)](#) [![OpenClaw Plugin](https://img.shields.io/badge/interface-OpenClaw_Plugin-black)](#) [![Skill](https://img.shields.io/badge/interface-Skill-black)](#) [![Universal Interface Spec](https://img.shields.io/badge/Universal_Interface_Spec-black?style=flat&color=black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-universal-installer/SPEC.md)

# 1Password Secrets

Give your AI secure access to 1Password. Never copy-paste an API key into a chat window again. Your agent reads secrets directly from the vault at runtime.

Works with Claude Code, OpenClaw, and any MCP-compatible agent. Also ships as a Node.js module you can import into your own tools. Fully headless via service accounts... no desktop app, no biometrics, no popups.

## Teach Your AI to Use 1Password Secrets

Open your AI and say:

```
Read the SKILL.md at github.com/wipcomputer/wip-1password/blob/main/SKILL.md.

Then explain to me:
1. What are these tools?
2. What do they do?
3. What would they change about how we work together?

Then ask me:
- Do you have more questions?
- Do you want to install them?

If I say yes, run: wip-install wipcomputer/wip-1password --dry-run

Show me exactly what will change on my system. When I'm ready, I'll tell you
to install for real.
```

Your agent will read the repo, explain everything, and do a dry-run install first so you can see exactly what changes before anything is written to your system.

## What It Does

1. **Your agent can read and write secrets** ... API keys, tokens, credentials. No more pasting.
2. **Works in Claude Code out of the box** ... MCP server connects automatically.
3. **Secrets stay off disk** ... Config files use references, real values only exist in memory.
4. **Debug without exposing secrets** ... Test connectivity and preview values safely.

## Documentation

- [TECHNICAL.md](TECHNICAL.md) ... Full setup guide, agent tools API, config resolution, CLI commands, developer guide, troubleshooting
- [SKILL.md](SKILL.md) ... Machine-readable skill definition for AI agents
- [Universal Interface Spec](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-universal-installer/SPEC.md) ... The six interfaces every agent-native tool can ship

## License

Dual-license model designed to keep tools free while preventing commercial resellers.

```
MIT      All CLI tools, MCP servers, skills, and hooks (use anywhere, no restrictions).
AGPLv3   Commercial redistribution, marketplace listings, or bundling into paid services.
```

AGPLv3 for personal use is free. Commercial licenses available.

### Can I use this?

**Yes, freely:**
- Use any tool locally or on your own servers
- Modify the code for your own projects
- Include in your internal CI/CD pipelines
- Fork it and send us feedback via PRs (we'd love that)

**Need a commercial license:**
- Bundle into a product you sell
- List on a marketplace (VS Code, JetBrains, etc.)
- Offer as part of a hosted/SaaS platform
- Redistribute commercially

Using these tools to build your own software is fine. Reselling the tools themselves is what requires a commercial license.

By submitting a PR, you agree to the [Contributor License Agreement](CLA.md).

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
