---
name: symbiont
description: Zero-trust AI agent governance for OpenClaw. Adds ORGA runtime, Cedar policy enforcement, SchemaPin tool verification, ClawHavoc skill scanning, and cryptographic audit trails. Use when you need agent governance, security policies, Cedar authorization, MCP tool verification, audit logging, or when scaffolding governed agent projects, scanning skills for malicious patterns, or writing Symbiont DSL definitions.
version: 0.1.0
metadata:
  clawdbot:
    emoji: "🛡️"
    requires:
      bins:
        - jq
      env: []
    install:
      - id: brew
        kind: brew
        formula: symbi
        tap: thirdkeyai/tap
        bins: [symbi]
        label: "Install symbi (Homebrew)"
    primaryEnv: ""
    homepage: https://symbiont.dev
    repository: https://github.com/thirdkeyai/symbi-openclaw
    tags:
      - security
      - governance
      - zero-trust
      - cedar
      - mcp
      - agent-runtime
      - policy-enforcement
      - audit
      - schemapin
      - enterprise
---

# Symbiont Governance for OpenClaw

Bring [Symbiont](https://symbiont.dev)'s zero-trust AI agent governance to your OpenClaw workflow. Enforce Cedar authorization policies, verify MCP tool integrity with SchemaPin, scan skills with ClawHavoc, maintain cryptographic audit trails, and manage governed agents.

This skill is the OpenClaw counterpart to [symbi-claude-code](https://github.com/thirdkeyai/symbi-claude-code) and [symbi-gemini-cli](https://github.com/thirdkeyai/symbi-gemini-cli). All three deliver the same Symbiont governance capabilities, adapted for each platform's skill/extension format.

A companion SOUL.md for the Symbiont governance agent personality is available separately on [onlycrabs.ai](https://onlycrabs.ai/jaschadub/symbiont).

## Prerequisites

- [OpenClaw](https://openclaw.ai) installed
- `jq` for JSON parsing (`apt install jq` / `brew install jq`)
- `symbi` binary on PATH (optional; skill degrades gracefully without it)

Install `symbi`:
```bash
# Via Homebrew (recommended)
brew tap thirdkeyai/tap && brew install symbi

# Or from source
cargo install symbi

# Or via Docker
docker pull ghcr.io/thirdkeyai/symbi:latest
```

## Quick Start

After installing this skill:

1. Tell the agent: **"Initialize a Symbiont-governed project"**
2. Define agents in `agents/*.dsl`
3. Create Cedar policies in `policies/*.cedar`
4. Ask the agent: **"Check Symbiont status"**

## Capabilities

This skill provides six governed workflows. Invoke them by describing what you need; the agent will follow the appropriate procedure.

### 1. Initialize a Governed Project

**Trigger**: "Set up Symbiont governance", "Initialize a governed project", "Add agent governance to this repo"

Create the governed project scaffold in the current directory:

1. Check if `symbiont.toml` already exists. If it does, confirm before overwriting.
2. Create directory structure:
   ```
   agents/          # Agent DSL definitions
   policies/        # Cedar policy files
   .symbiont/       # Local governance config and audit logs
   .symbiont/audit/ # Audit log output
   ```
3. Write `symbiont.toml` with defaults:
   ```toml
   [runtime]
   security_tier = "tier1"
   log_level = "info"

   [policy]
   engine = "cedar"
   enforcement = "strict"

   [schemapin]
   mode = "tofu"
   ```
4. Write a starter agent at `agents/assistant.dsl`:
   ```symbiont
   metadata {
       version = "1.0.0"
       description = "Default governed assistant"
   }

   agent assistant(input: Query) -> Response {
       capabilities = ["read", "analyze"]

       policy default_access {
           allow: read(input) if true
           deny: write(any) if not approved
           audit: all_operations
       }

       with memory = "session" {
           result = process(input)
           return result
       }
   }
   ```
5. Write a starter Cedar policy at `policies/default.cedar`:
   ```cedar
   permit(
       principal,
       action == Action::"read",
       resource
   );

   forbid(
       principal,
       action == Action::"write",
       resource
   ) unless {
       principal.approved == true
   };
   ```
6. Write `.symbiont/local-policy.toml` with default deny rules:
   ```toml
   [deny]
   paths = [".env", ".ssh/", ".aws/", ".gnupg/", "credentials"]
   commands = ["rm -rf", "git push --force", "mkfs", "dd if="]
   branches = ["main", "master", "production"]
   ```
7. Write `AGENTS.md` manifest.
8. Report what was created and suggest next steps.

### 2. Create or Edit Cedar Policies

**Trigger**: "Create a Cedar policy", "Edit authorization policy", "Add a policy for X"

Steps:
1. Ask what the policy should govern (read/write access, tool invocation, sandbox tier, etc.).
2. Check existing policies in `policies/*.cedar`.
3. Write or update the `.cedar` file using Cedar syntax.
4. If `symbi` is on PATH, validate with `symbi policy validate policies/`.
5. Explain what the policy permits and forbids.

Reference: Read `references/cedar-patterns.md` for common Cedar policy patterns.

### 3. Verify MCP Tool Schemas (SchemaPin)

**Trigger**: "Verify this MCP tool", "Check tool schema", "Is this tool signed?"

Steps:
1. Identify the tool name and domain.
2. If `symbi` is on PATH, run `symbi verify --tool <tool_name> --domain <domain>`.
3. Otherwise, explain SchemaPin's ECDSA P-256 verification model and suggest manual steps.
4. Report verification result: signature valid/invalid, TOFU pin status, revocation status.

### 4. Query Audit Logs

**Trigger**: "Show audit logs", "What did the agent do?", "Review tool usage"

Steps:
1. Check for `.symbiont/audit/tool-usage.jsonl`.
2. Parse JSONL entries and summarize: tool name, timestamp, action, result, policy decision.
3. If `symbi` is on PATH, use `symbi audit query` for richer queries.
4. Highlight any denied or flagged operations.

### 5. Write or Validate DSL Agent Definitions

**Trigger**: "Create an agent definition", "Write a DSL agent", "Validate my agent DSL"

Steps:
1. Determine agent purpose, capabilities, and policy requirements.
2. Write or edit the `.dsl` file in `agents/`.
3. If `symbi` is on PATH, validate with `symbi dsl parse agents/<name>.dsl`.
4. Update `AGENTS.md` manifest.

Reference: Read `references/dsl-guide.md` for DSL syntax and patterns.

### 6. Scan Skills for Malicious Patterns (ClawHavoc)

**Trigger**: "Scan this skill", "Is this skill safe?", "Check for malicious patterns", "ClawHavoc scan"

Steps:
1. Identify the skill directory or SKILL.md to scan.
2. Run `scripts/clawhavoc-scan.sh <skill-path>` to check against 40+ built-in detection rules.
3. Report findings by severity: Critical, High, Medium, Warning, Info.
4. Critical or High findings mean the skill should NOT be loaded.
5. Suggest remediation for any findings.

The scanner covers: reverse shells, credential harvesting, network exfiltration, process injection, privilege escalation, symlink/path traversal, and downloader chains.

## Governance Tiers

This skill provides three progressive levels of protection, matching `symbi-claude-code` and `symbi-gemini-cli`:

### Tier 1: Awareness (default)

All tool calls proceed. State-modifying actions are logged to `.symbiont/audit/tool-usage.jsonl` for post-hoc review.

No `symbi` binary required. The `scripts/audit-log.sh` script handles logging.

### Tier 2: Protection

Create `.symbiont/local-policy.toml` to block dangerous patterns:

```toml
[deny]
paths = [".env", ".ssh/", ".aws/"]
commands = ["rm -rf", "git push --force"]
branches = ["main", "master", "production"]
```

The `scripts/policy-guard.sh` script checks tool calls against this deny list. Built-in patterns (destructive commands, force pushes, writes to sensitive files) are always blocked regardless of config.

No `symbi` binary required. The same `.symbiont/local-policy.toml` works across symbi-claude-code, symbi-gemini-cli, and this skill.

### Tier 3: Governance

If `symbi` is on PATH and `policies/` exists, Cedar policies are evaluated for formal authorization decisions on every tool call.

## Dual-Mode Architecture

### Mode A: Standalone (Skill-First)

Developer installs this skill into OpenClaw. The skill provides advisory policy checking, audit logging, and access to Symbiont MCP tools if `symbi` is on PATH.

```
Developer -> OpenClaw + symbiont skill -> symbi mcp (stdio)
```

Best for: individual developers adding governance awareness to their workflow.

### Mode B: ORGA-Managed (Runtime-First)

Symbiont's CliExecutor spawns OpenClaw as a governed subprocess. The skill detects `SYMBIONT_MANAGED=true` and connects back to the parent runtime's MCP server instead of spawning a new one. The outer ORGA Gate provides hard enforcement that cannot be bypassed.

```
Symbiont Runtime (ORGA Loop)
  -> CliExecutor (sandbox + budget enforcement)
    -> OpenClaw (with symbiont skill)
      -> Skill connects back to parent MCP server
```

Best for: automated pipelines, dark factory deployments, enterprise governance.

## Rules

- ALWAYS check `.symbiont/local-policy.toml` before executing commands that modify files, run shell commands, or interact with git branches.
- ALWAYS log state-modifying tool calls to `.symbiont/audit/tool-usage.jsonl`.
- NEVER execute commands matching deny patterns in the local policy.
- NEVER write to paths listed in the deny list (`.env`, `.ssh/`, `.aws/`, etc.).
- NEVER force-push to protected branches.
- If `SYMBIONT_MANAGED=true` is set in the environment, defer all policy decisions to the parent Symbiont runtime via MCP.
- When scanning skills with ClawHavoc, ALWAYS refuse to load skills with Critical or High findings.
- When verifying tools with SchemaPin, ALWAYS warn the user if a tool's signature is invalid or its key has been revoked.

## File Conventions

| Path | Purpose |
|------|---------|
| `agents/*.dsl` | Agent DSL definitions |
| `policies/*.cedar` | Cedar authorization policies |
| `symbiont.toml` | Symbiont runtime configuration |
| `AGENTS.md` | Agent manifest |
| `.symbiont/audit/` | Audit log output |
| `.symbiont/local-policy.toml` | Local deny list (Tier 2) |

## Comparison with Other Symbiont Plugins

| Aspect | Claude Code | Gemini CLI | OpenClaw |
|--------|-------------|------------|----------|
| Format | Plugin (`.claude-plugin/`) | Extension (`gemini-extension.json`) | Skill (`SKILL.md`) |
| Commands | Markdown files | TOML files | Natural language triggers |
| MCP tool prefix | `mcp__symbi__` | `symbi__` | `symbi__` (when connected) |
| Native policies | No | Yes (`policies/*.toml`) | No |
| Tool restriction | Allow list | Deny list (`excludeTools`) | Deny list (`.symbiont/local-policy.toml`) |
| Context file | `CLAUDE.md` | `GEMINI.md` | `SOUL.md` (via onlycrabs.ai) |
| Skill scanning | Via hook | Via hook | Built-in ClawHavoc scanner |

## Links

- [Symbiont Documentation](https://docs.symbiont.dev)
- [ThirdKey AI](https://thirdkey.ai)
- [SchemaPin](https://schemapin.org)
- [AgentPin](https://agentpin.org)
- [Claude Code Plugin](https://github.com/thirdkeyai/symbi-claude-code)
- [Gemini CLI Extension](https://github.com/thirdkeyai/symbi-gemini-cli)

## License

Apache 2.0

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by Anthropic PBC, Google LLC, or the OpenClaw project. "OpenClaw" and "ClawHub" are trademarks of their respective owners. "Symbiont" and "ThirdKey" are trademarks of ThirdKey AI.
