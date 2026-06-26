# {{skill_name}}

**Skill wrapping external tools/scripts for [purpose].**

## When to Use

Activate when the user wants to:
- [Tool-specific action 1]
- [Tool-specific action 2]
- [Tool-specific action 3]

## Prerequisites

- Tool/script installed at: `[path]`
- Required permissions: `[permissions]`
- Environment variables: `[if needed]`

## Workflow

### Preparation
1. **Validate Environment:** Check tool availability and version
2. **Validate Inputs:** Ensure required parameters are present
3. **Safety Check:** Confirm no destructive operations without user approval

### Execution
4. **Build Command:** Construct tool invocation with validated parameters
5. **Preview:** Show user the exact command/script that will run
6. **Execute:** Run only after explicit confirmation
7. **Parse Output:** Extract relevant information
8. **Present Results:** Format output for readability

### Cleanup
9. **Verify:** Ensure expected outcomes were achieved
10. **Document:** Log results in session notes if significant

## Tools / Scripts

| Script | Purpose | Safety Notes |
|--------|---------|--------------|
| `scripts/{{script_name}}.py` | [What it does] | [What to watch for] |

## Examples

### Example 1: Successful Execution

**User:** *"[Request using this tool]"*

**Skill:**
1. Checks prerequisites ✅
2. Builds command: `[command preview]`
3. **Asks:** *"Soll ich das ausführen?"*
4. On confirmation → executes → presents results

### Example 2: Missing Prerequisites

**User:** *"[Request when tool not ready]"*

**Skill:** Identifies missing prerequisite, guides user to install/configure

## Safety & Boundaries

### NEVER
- Execute commands with sudo/admin privileges without explicit warning
- Delete files as part of "cleanup" without confirmation
- Pipe untrusted input directly into commands
- Run network operations without user awareness

### ALWAYS
- Show the exact command before executing
- Validate inputs (path exists, format correct)
- Check return codes and handle errors
- Explain what a command does if it's complex

## Metadata

- **Version:** 1.0.0
- **Created:** {{date}}
- **Requires:** [tool name] [version]
- **Tags:** [tool, automation]
