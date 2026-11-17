## Description:

Generates a verifiable Chinese task handoff package from one structured task contract, with human and AI Markdown views and an offline ZIP manifest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and collaborators use this skill to turn a confirmed Chinese task contract into a handoff package that people and AI agents can read and verify from the same source. It is suited for task handoff, outsourcing coordination, and human-AI scope confirmation, not for carrying full chat history or replacing environment revalidation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task contracts may expose sensitive information if users include secrets, full chat logs, customer data, or large private files.

Mitigation: Keep the contract minimal, avoid secrets and full chat/customer data, and use versioned references or hashes for larger source material.

Risk: Permissions written inside the package could be mistaken for current approval to perform external, paid, publishing, or irreversible actions.

Mitigation: Treat package permissions as task notes and obtain current user approval before any real-world or irreversible action.

Risk: Incomplete completion criteria or unresolved open questions can cause people and agents to proceed with different assumptions.

Mitigation: Review the generated contract and Markdown views before sharing; leave unknowns in open questions and regenerate from the contract instead of editing projections manually.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongsheng123132/skills/task-sync-pack)
- [Project homepage](https://github.com/dongsheng123132/task-sync-pack)
- [Task contract schema](https://taskpack.org/schema/task-sync/1/task-contract.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON contract, Markdown task views, manifest, and .task-sync.zip archive]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local rendering with SHA-256 manifest checks and offline verification.]

## Skill Version(s):

0.1.1 (source: server release evidence, frontmatter, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
