## Description: <br>
Scan constraint files across AI coding platforms, identify rules enforceable by tools, and auto-generate linters, hooks, validators, and wrapper functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dachunggan](https://clawhub.ai/user/dachunggan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert prompt-level project rules from Claude Code, OpenClaw, Cursor, Copilot, and similar agent environments into enforceable tooling. It is intended for new project setup, existing codebase onboarding, and rule automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite authoritative agent rule files and generate hooks that may run automatically. <br>
Mitigation: Require a reviewed diff before edits to CLAUDE.md, agents.md, soul.md, tools.md, bootstrap.md, .cursorrules, or Copilot instructions, and review generated hooks as executable code. <br>
Risk: Source-rule removal could weaken project constraints if generated tooling does not preserve the original intent. <br>
Mitigation: Do not allow removal of source rules unless the generated tooling fully preserves the original intent and the user has approved the change. <br>


## Reference(s): <br>
- [Rule Toolkit on ClawHub](https://clawhub.ai/dachunggan/rule-toolkit) <br>
- [OpenClaw Hooks Reference](references/openclaw-hooks.md) <br>
- [Tool Generation Patterns](references/tool-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports with generated code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or create linters, hooks, validators, wrapper functions, and updates to agent constraint files for user review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
