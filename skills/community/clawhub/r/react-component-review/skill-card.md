## Description:

Review a React/TypeScript component for correctness, hook safety, prop modeling, accessibility, state coverage, and minimal safe changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ritual](https://clawhub.ai/user/ritual)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review React/TypeScript components for correctness, hook safety, prop and state modeling, accessibility, state coverage, and minimal safe changes before merging or shipping UI code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Ritual Cloud setup can expand the review context beyond the files directly provided to the agent.

Mitigation: Use the skill in local mode unless broader workspace context is needed; before enabling Ritual Cloud, review what the CLI will access or send during initialization.

Risk: Installing the optional cloud CLI without controls can introduce avoidable local tooling risk.

Mitigation: Pin the CLI version where practical, run it without administrator privileges, and verify CLI status before using the cloud path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ritual/skills/react-component-review)
- [Ritual homepage](https://ritual.work)
- [Publisher profile](https://clawhub.ai/user/ritual)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown review with verdict, grouped findings, optional minimal patches, and verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise TypeScript/React code patches and exact local checks such as tests, Storybook, lint, typecheck, or smoke verification.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
