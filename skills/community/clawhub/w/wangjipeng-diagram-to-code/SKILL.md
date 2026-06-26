---
name: diagram-to-code
description: >
  Use when (1) user provides architecture diagram and needs infrastructure as code or component code. 
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

# Diagram To Code

Use when (1) user provides architecture diagram and needs infrastructure as code or component code. 

## Core Position

This skill solves the specific engineering problem of: *user provides architecture diagram and needs infrastructure as code or component code*

This skill is NOT:
- A general-purpose capability that activates on anything
- A replacement for manual human judgment
- A tool that stores state or remembers across sessions

This skill IS activated ONLY when the trigger conditions are explicitly met.

## Modes

### `/diagram-to-code`

**Default mode.** Performs the core task end-to-end.

When to use: User provides input matching the trigger conditions above.


## Execution Steps

1. **Receive diagram** — User pastes an architecture diagram, flowchart, or infrastructure plan
   - Accepted formats: Mermaid, PlantUML, draw.io XML, ASCII art, or a text description
   - If the input is not recognizable as a diagram, state: "This skill converts architecture diagrams to infrastructure as code or component code. Please provide a diagram in Mermaid, PlantUML, or draw.io format."

2. **Parse diagram structure** — Identify the diagram elements:
   - Detect nodes (services, components, databases, queues)
   - Identify relationships (arrows, dependencies, data flows)
   - Note labels, annotations, and any numeric values (latency, throughput)
   - Determine the diagram type (architecture, flowchart, sequence, ER)

3. **Map to target code form** — Identify the appropriate output:
   - Infrastructure diagrams → Terraform (.tf), Kubernetes YAML, or CloudFormation
   - Flowcharts → state machine code, workflow scripts, or sequence diagrams
   - Component diagrams → code structure (React components, Python classes)
   - Network diagrams → config files or deployment manifests

4. **Generate code** — Produce the target format with the diagram's structure:
   - Use correct syntax for the target platform (HCL for Terraform, YAML for K8s)
   - Name resources based on node labels in the diagram
   - Add comments linking each code block back to the diagram element
   - Include realistic defaults for unstated properties

5. **Deliver with validation** — Return the code with a diagram-to-code mapping:
   - List each diagram node and the corresponding code resource
   - Note any assumptions made for unlabeled properties
   - If multiple output formats are possible, state which was chosen and why
   - Offer to refine specific components or add missing connections

## Mandatory Rules

### Do not

- Do not make up facts or claim actions were taken that were not
- Do not hardcode API keys — use `os.getenv("API_KEY")` instead
- Do not store sensitive user data beyond the current session
- Do not exceed token budget without warning the user first
- Do not activate for off-topic requests — return a brief decline message

### Do

- Validate all inputs before acting
- Handle errors gracefully with actionable error messages
- Log actions taken for auditability
- State explicitly when you are uncertain or data is insufficient

## Quality Bar

**A good output:**
- Solves exactly the problem described in the trigger conditions
- Provides actionable result in the expected format within 3 turns
- Handles error cases with specific guidance, not generic "try again"
- States assumptions explicitly when input is ambiguous

**A bad output:**
- Solves a different problem than the one triggered
- Provides a generic "I can't help with that" without explaining why
- Crashes, hangs, or returns malformed output on valid input
- Activates for off-topic requests (false positive)

## Good vs. Bad Examples

| Scenario | Bad Output | Good Output |
|---|---|---|
| Trigger matched | "I can help with that." + no action | Correct transformation delivered in structured format |
| Invalid input | Crash or wrong result | "Missing required field: [X]. Please provide [Y]." |
| Ambiguous input | Guesses and might be wrong | States assumption and asks for confirmation |
| Off-topic request | Attempts to help anyway | "This skill activates when [trigger]. Please restate your request." |

## References

- `references/` — Detailed templates, schemas, and edge-case rules for this skill
