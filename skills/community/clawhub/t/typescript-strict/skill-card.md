## Description:

Deep TypeScript strictness workflow for incremental enablement, compiler flags, typing boundaries, narrowing, generics, utility types, and safe refactors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and execute incremental TypeScript strictness adoption, reduce `any`, improve IO boundary typing, and add CI guardrails in large or legacy TypeScript codebases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compiler flag or TypeScript configuration changes can affect many packages and block builds when applied broadly.

Mitigation: Capture a baseline `tsc --noEmit` error count, apply stricter flags by package or path, and review changes before merging.

Risk: Recommended CI or lint guardrails can disrupt existing development workflows if enabled all at once.

Mitigation: Introduce gates incrementally, start with changed-code checks where appropriate, and require human review for CI configuration changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawkk/skills/typescript-strict)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, checklists, and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
