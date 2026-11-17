## Description:

Python Flow Engine is a lightweight Python flow orchestration library for serial, parallel, and conditional data-processing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dnaxxx-hub](https://clawhub.ai/user/dnaxxx-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Python data pipelines, ETL workflows, and multi-step automations with serial, parallel, conditional, retry, timeout, and Mermaid visualization support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Node callables execute in process and can perform any side effects available to the running Python process.

Mitigation: Run only trusted callables and review pipeline code before deployment.

Risk: Timeout behavior is advisory and may not stop side-effecting work after a timeout is reported.

Mitigation: Do not rely on the timeout setting to stop file writes, API calls, database updates, or expensive computation; use idempotent tasks and external cancellation controls where needed.

## Reference(s):

- [Python Flow Engine ClawHub page](https://clawhub.ai/dnaxxx-hub/skills/python-flow-engine)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python code snippets, shell commands, and Mermaid flowchart text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reusable Python pipeline code and examples; pipeline visualization output is Mermaid-compatible text.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
