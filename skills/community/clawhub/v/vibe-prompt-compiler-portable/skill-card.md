## Description:

Compile rough natural-language coding requests into structured, high-signal prompts for cross-platform AI coding tools such as Cursor, Claude Code, Codex CLI, Gemini CLI, and generic IDE chat assistants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiyuequkanhai](https://clawhub.ai/user/qiyuequkanhai)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to turn vague coding or product-engineering requests into scoped implementation briefs, handoff prompts, assumptions, non-goals, constraints, and acceptance criteria for AI coding tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated handoff prompts may carry incorrect assumptions into another coding agent.

Mitigation: Review generated prompts and handoffs before pasting them into another tool, especially for broad, architecture, auth, data, or production tasks.

Risk: Repo-aware mode can read common local repository files to infer coding rules.

Mitigation: Run repo-aware extraction only in repositories the user intends to analyze, and review the extracted rules before use.

Risk: The package includes local executable Python helper scripts.

Mitigation: Inspect and run the scripts in a trusted local environment before adding them to routine workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiyuequkanhai/skills/vibe-prompt-compiler-portable)
- [Auto mode](references/auto-mode.md)
- [Portable usage](references/usage.md)
- [Portable prompt templates](references/templates.md)
- [Routing rules](references/routing.md)
- [Tool examples](references/tool-examples.md)
- [Real examples](references/real-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, and plain text prompts with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured handoff briefs, prompt-lint guidance, tool-specific wrapper text, and repository-aware rule summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
