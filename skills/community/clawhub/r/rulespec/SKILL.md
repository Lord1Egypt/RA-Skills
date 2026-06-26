---
name: rulespec
description: >
  Define, manage, and compile business rules as structured YAML data into LLM-ready prompts and agent-loadable SKILL.md files.
  Use when the user wants to create business rules, define policies, set guardrails, enforce constraints, add compliance rules,
  manage refund policies, escalation rules, approval thresholds, SLA requirements, content moderation rules, or any operational
  policy an AI agent should follow. Also use when the user says "add a rule", "create a policy", "set a constraint",
  "define guardrails", or asks about rulespec, rulespec.yaml, or business rule management.
---

# rulespec

**Manage business rules for AI agents without breaking what already works.**

Adding a rule to a system prompt shouldn't risk invalidating the ones that are already there. Inline prompt editing doesn't scale — and other solutions aren't built for business rules.

rulespec treats each rule as an independent, validated unit. Add, edit, or remove one rule via CLI — the rest stay untouched. The output is a structured SKILL.md that any AI agent can load.

**IMPORTANT: Always use the `rulespec` CLI to modify rules, sources, and examples. Never edit emitted SKILL.md files directly — they are generated and will be overwritten.** For complex structures (source schemas, nested example data), you may edit `rulespec.yaml` directly, but always run `rulespec validate` afterward.

All commands use `npx rulespec` — no global install needed. npx downloads and runs it automatically.

## CLI commands

### Setup
```bash
rulespec init --domain "invoice processing"   # Create rulespec.yaml with domain
rulespec set-domain "customer support"         # Change the domain
```

### Rules
```bash
rulespec add --id <id> --rule <text> --context <text> --intent <enforce|inform|suggest>
rulespec edit <id> --rule <new text>           # Update rule text
rulespec edit <id> --intent enforce            # Change intent level
rulespec edit <id> --context "new context"     # Change when rule applies
rulespec remove <id>                           # Remove a rule
rulespec list                                  # List all rules
```

### Sources
```bash
rulespec add-source --id <id> --type <document|api|database|message|structured> --description <text> [--format <fmt>]
rulespec remove-source <id>
```

### Global examples (end-to-end input/output pairs)
```bash
rulespec add-example --input '{"key": "val"}' --output '{"key": "val"}' [--note <text>]
rulespec add-example --input /path/to/input.json --output /path/to/output.json --note "From files"
rulespec add-example --input /path/to/invoice.pdf --output '{"action": "approve"}' --note "PDF input"
rulespec remove-example <index>                # 0-based index
```

### Rule-specific examples
```bash
rulespec add-rule-example <rule-id> --input '{"amount": 100}' --output '{"approved": true}'
rulespec add-rule-example <rule-id> --input /path/to/file.pdf --output '{"extracted": "data"}'
rulespec remove-rule-example <rule-id> <index> # 0-based index
```

### Input/output resolution

Both `--input` and `--output` accept three formats:
- **Inline JSON**: `'{"key": "val"}'` — parsed directly
- **JSON file path**: `/path/to/data.json` — file is read and parsed
- **Any other file path**: `/path/to/doc.pdf` — stored as `{ file: "/path/to/doc.pdf" }`

### Find & replace
```bash
rulespec replace --old "30 days" --new "60 days"   # Validates + recompiles automatically
```

### Build & emit
```bash
rulespec compile [id]                          # Preview compiled prompts
rulespec validate                              # Check file against schema
rulespec emit                                  # Generate skills/{domain}/SKILL.md
rulespec emit --include-examples true          # Include examples in output
rulespec emit --outdir <path>                  # Custom output dir (default: skills)
```

All commands accept `--file <path>` to specify a different file (default: `rulespec.yaml`).

## File format

```yaml
schema: rulespec/v1
domain: "your domain here"

sources:                              # optional — what data the rules operate on
  - id: source-name
    type: document | api | database | message | structured
    format: pdf | json | csv          # optional
    description: "What this source is"
    schema:                           # optional — shape of the data
      field: type

rules:
  - id: rule-id                       # kebab-case, unique
    rule: "The business rule in plain language"
    context: "When this rule applies"
    intent: enforce | inform | suggest

examples:                             # optional — end-to-end golden standards
  - note: "What this example tests"
    input: { ... }
    output: { ... }
```

### Intent levels

- `enforce` — mandatory. Agent must follow this rule. Compiles to directive language.
- `inform` — guidance. Agent should be aware. Compiles to neutral language.
- `suggest` — recommendation. Agent may consider. Compiles to soft language.

## Workflow

1. `rulespec init --domain "my domain"` to create the file
2. Add sources with `rulespec add-source`
3. Add rules with `rulespec add`
4. Add examples with `rulespec add-example`
5. `rulespec validate` to check for errors
6. `rulespec compile` to preview compiled prompts
7. `rulespec emit` to generate `skills/{domain}/SKILL.md`

## Programmatic usage

To inject rules into LLM prompts at runtime:

```typescript
import { loadRules } from "rulespec";
const rules = await loadRules("rulespec.yaml");
// rules is a compiled markdown string — inject into any system prompt or API call
```

## Key principles

- Use the CLI for rules, sources, and examples — never edit emitted SKILL.md files
- For complex source schemas or nested example data, edit `rulespec.yaml` directly + run `rulespec validate`
- `rulespec replace` is a safe find-and-replace: validates and recompiles after every change
- One rule, one change — editing a rule only affects that rule's compiled output
- Examples are excluded from emitted SKILL.md by default (they may contain sensitive data)

Built by the team behind [Clawnify](https://www.clawnify.com).
