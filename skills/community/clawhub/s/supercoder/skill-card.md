## Description: <br>
Supercoder guides an agent through a six-phase workflow for analyzing a requirement, exploring the codebase, clarifying implementation choices, designing an approach, implementing code, and verifying the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unfallenwill](https://clawhub.ai/user/unfallenwill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when a user provides a requirement, PRD, specification, or feature request and expects end-to-end delivery against an existing codebase. It structures the work from discovery through verification, with user checkpoints for clarification, design selection, and final confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to edit files and run local commands during implementation work. <br>
Mitigation: Use version control, review diffs, and give explicit limits before allowing broad edits, destructive commands, or commands derived from untrusted requirements or URLs. <br>
Risk: The workflow may fetch requirement content from a URL when the user provides one. <br>
Mitigation: Treat fetched requirements as untrusted input and confirm scope, design choices, and command execution before implementation. <br>


## Reference(s): <br>
- [Discover phase](references/discover-phase.md) <br>
- [Explore phase](references/explore-phase.md) <br>
- [Clarify phase](references/clarify-phase.md) <br>
- [Design phase](references/design-phase.md) <br>
- [Implement phase](references/implement-phase.md) <br>
- [Verify phase](references/verify-phase.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational Markdown with code, shell commands, file changes, task updates, questions, and verification summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May edit files, run local commands, fetch requirement URLs, and delegate exploration or design work to subagents when the host agent supports those tools.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
