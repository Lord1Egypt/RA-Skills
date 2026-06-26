## Description: <br>
Compile rough natural-language coding requests into structured, high-signal prompts for cross-platform AI coding tools such as Cursor, Claude Code, Codex CLI, Gemini CLI, and generic IDE chat assistants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiyuequkanhai](https://clawhub.ai/user/qiyuequkanhai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to turn vague coding or product-engineering requests into scoped implementation briefs with assumptions, constraints, non-goals, and acceptance criteria. It is best suited for MVPs, bugfixes, refactors, architecture reviews, integrations, automation workflows, and cross-tool handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The compiler may turn a broad or vague request into a scoped brief whose assumptions do not match the user's intent. <br>
Mitigation: Review the generated assumptions, scope, non-goals, and acceptance criteria before using the brief to drive implementation. <br>
Risk: Repository-aware options can read local project guidance files such as README, AGENTS.md, and package.json. <br>
Mitigation: Use repo-aware flags only on repositories whose local guidance and metadata files are appropriate for the helper script to read. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qiyuequkanhai/vibe-prompt-compiler-portable) <br>
- [Auto Mode](references/auto-mode.md) <br>
- [Templates](references/templates.md) <br>
- [Routing](references/routing.md) <br>
- [Usage](references/usage.md) <br>
- [Tool Examples](references/tool-examples.md) <br>
- [Real Examples](references/real-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON, and command-line snippets depending on workflow mode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task classification, assumptions, scope, non-goals, acceptance criteria, tool-specific handoff wrappers, Chinese-first output, and repository-aware rules when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
