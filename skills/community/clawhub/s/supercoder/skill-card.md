## Description:

Supercoder guides an agent through a six-phase requirement-to-code workflow for analyzing feature requests, designing an implementation, editing project files, and verifying the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unfallenwill](https://clawhub.ai/user/unfallenwill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Supercoder when they have a requirement, PRD, specification, or feature request and want an agent to move through discovery, codebase exploration, clarification, design, implementation, and verification with user checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to edit project files and run repository-defined tests during implementation.

Mitigation: Use it only for intended feature delivery, review the design checkpoint before implementation, and monitor command execution in sensitive repositories.

Risk: Repository-defined test or build steps may execute risky or sensitive operations.

Mitigation: Review planned verification commands before they run, especially in repositories with untrusted scripts or sensitive build steps.

## Reference(s):

- [Phase 1: Discover](references/discover-phase.md)
- [Phase 2: Explore](references/explore-phase.md)
- [Phase 3: Clarify](references/clarify-phase.md)
- [Phase 4: Design](references/design-phase.md)
- [Phase 5: Implement](references/implement-phase.md)
- [Phase 6: Verify](references/verify-phase.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with code changes, implementation plans, verification summaries, and inline shell commands as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit project files and run repository-defined tests as part of user-directed feature delivery.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
