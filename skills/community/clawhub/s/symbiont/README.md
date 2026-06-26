# symbi-openclaw

Zero-trust AI agent governance for [OpenClaw](https://openclaw.ai). Brings [Symbiont](https://symbiont.dev)'s ORGA runtime, Cedar policy enforcement, SchemaPin tool verification, ClawHavoc skill scanning, and cryptographic audit trails to OpenClaw workflows.

## Install

**From ClawHub:**
```bash
clawhub install jaschadub/symbiont
```

**From GitHub:**
```bash
clawhub install https://github.com/thirdkeyai/symbi-openclaw
```

**Manual:**
Copy this directory to `~/.openclaw/skills/symbiont/` or your workspace's `skills/` directory.

## What You Get

- **Three governance tiers**: Awareness (logging) -> Protection (deny list) -> Governance (Cedar policies)
- **ClawHavoc scanner**: 40+ detection rules across 10 attack categories
- **Cedar policy management**: Create, edit, and validate authorization policies
- **SchemaPin verification**: Cryptographic MCP tool schema verification
- **Cryptographic audit trails**: JSONL logging of all state-modifying tool calls
- **Symbiont DSL**: Write and validate governed agent definitions
- **Dual-mode architecture**: Standalone (Mode A) or ORGA-managed (Mode B)

## Usage

After installing, tell your OpenClaw agent what you need:

| Say this | Agent does this |
|----------|-----------------|
| "Initialize a Symbiont-governed project" | Scaffolds `agents/`, `policies/`, `.symbiont/`, config files |
| "Create a Cedar policy for read-only access" | Writes a `.cedar` file with appropriate rules |
| "Verify this MCP tool's schema" | Runs SchemaPin ECDSA P-256 verification |
| "Show me the audit logs" | Parses and summarizes `.symbiont/audit/tool-usage.jsonl` |
| "Write a DSL agent definition for a scanner" | Creates a `.dsl` file with policies and capabilities |
| "Scan this skill for malicious patterns" | Runs ClawHavoc 40-rule scanner, reports findings |
| "Check Symbiont status" | Reports on binary, config, policies, agents, audit state |

## Directory Structure

```
symbiont/                                 # ClawHub: jaschadub/symbiont
├── SKILL.md                              # Main skill definition
├── README.md                             # This file
├── LICENSE.md                            # Apache 2.0
├── CHANGELOG.md
├── agents/
│   ├── symbi-governor.md                 # Default governance agent persona
│   └── symbi-dev.md                      # DSL/Cedar development persona
├── scripts/
│   ├── policy-guard.sh                   # Tier 2: deny list enforcement
│   ├── audit-log.sh                      # Tier 1: tool usage logging
│   ├── clawhavoc-scan.sh                 # ClawHavoc skill scanner (40+ rules)
│   ├── symbi-status.sh                   # Runtime health check
│   └── mcp-connect.sh                    # Dual-mode MCP transport switching
├── references/
│   ├── cedar-patterns.md                 # Cedar policy patterns reference
│   └── dsl-guide.md                      # Symbiont DSL syntax reference
├── policies/
│   └── default-local-policy.toml         # Default deny list template
└── examples/
    ├── standalone/README.md
    ├── cli-executor/
    │   ├── README.md
    │   ├── openclaw-governed-dsl.md      # Example DSL agent definition
    │   └── default-cedar.md              # Example Cedar policy
    └── agent-sdk/README.md
```

Companion SOUL.md published separately on [onlycrabs.ai/jaschadub/symbiont](https://onlycrabs.ai/jaschadub/symbiont).

## Sibling Projects

This skill delivers the same governance capabilities as:

| Plugin | Platform | Repo |
|--------|----------|------|
| **symbi-claude-code** | Claude Code | [github.com/thirdkeyai/symbi-claude-code](https://github.com/thirdkeyai/symbi-claude-code) |
| **symbi-gemini-cli** | Gemini CLI | [github.com/thirdkeyai/symbi-gemini-cli](https://github.com/thirdkeyai/symbi-gemini-cli) |
| **symbiont** | OpenClaw | This repo (ClawHub: jaschadub/symbiont) |

The same `.symbiont/local-policy.toml` deny list works across all three.

## Security

This skill was built in direct response to the ClawHavoc attack (January 2026), which planted 341+ malicious skills on ClawHub delivering the Atomic macOS Stealer. The ClawHavoc scanner included in this skill detects the exact attack patterns used in that incident, plus broader categories of malicious behavior.

For cryptographic skill signing, see [SchemaPin v1.3.0](https://schemapin.org) which provides ECDSA P-256 signatures over skill folders (`.schemapin.sig`).

## Links

- [Symbiont Documentation](https://docs.symbiont.dev)
- [ThirdKey AI](https://thirdkey.ai)
- [SchemaPin](https://schemapin.org)
- [AgentPin](https://agentpin.org)

## License

Apache 2.0

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by Anthropic PBC, Google LLC, or the OpenClaw project. "OpenClaw" and "ClawHub" are trademarks of their respective owners. "Symbiont" and "ThirdKey" are trademarks of ThirdKey AI.
