## Description:

Audit React components for performance, accessibility, hook correctness, prop design, and re-render optimization \u2014 identify memo opportunities and state management issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to audit React components and custom hooks for performance, accessibility, hook correctness, prop design, and state-management issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs to read parts of a React source tree to produce useful review findings.

Mitigation: Use it only in repositories where source review is intended, and limit any discovery commands to the relevant project directories.

Risk: Audit findings and remediation suggestions may be incomplete or incorrect for the application's runtime behavior.

Mitigation: Review findings before making changes and verify accepted changes with project tests, linting, type checks, and accessibility checks.

Risk: Suggested shell commands search component files and may reveal source paths or snippets in the agent transcript.

Mitigation: Inspect commands before running them and avoid including sensitive source directories when requesting an audit.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown audit report with prioritized findings and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source locations, severity groupings, and concise remediation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
