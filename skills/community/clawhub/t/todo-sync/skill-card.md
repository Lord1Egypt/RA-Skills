## Description:

Helps users address unsynchronized to-dos between Enterprise WeChat and Feishu tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neutronstar238](https://clawhub.ai/user/neutronstar238)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can invoke this skill when they need help planning or operating a workflow for keeping Enterprise WeChat to-dos and Feishu tasks aligned. The current artifact is a minimal stub and does not yet implement core sync behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact is an unfinished sync stub, so users may assume automated synchronization exists before core behavior is implemented.

Mitigation: Review the installed version before deployment and confirm that the sync workflow, tests, and documentation are present.

Risk: Future versions may handle task-system credentials, background sync, or broad write access to task systems.

Mitigation: Review future versions for API credential handling, explicit permission boundaries, and write-scope limits before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neutronstar238/skills/todo-sync)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown or plain text responses with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No implementation-specific output contract is documented.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
