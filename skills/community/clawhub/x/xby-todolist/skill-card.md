## Description:

Provides external work memory and task management for large language models and AI agents to support reliable complex multi-step work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to maintain a session-level task list through a remote task-memory service, including reading current todos and writing structured todo updates during multi-step work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions are sent to a third-party remote task-memory provider.

Mitigation: Avoid putting secrets, private code, incident details, or personal data into todos unless the provider's privacy and retention terms are acceptable.

Risk: The API key can be saved in a plaintext .env file.

Mitigation: Store the API key outside shared repositories when possible and ensure .env is ignored by version control.

Risk: Security review flagged stale gaokao references and unpinned dependencies as production-readiness concerns.

Mitigation: Review those references and dependency constraints before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/xby-todolist)
- [XiaoBenYang API key site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY credential and returns remote todo data for the agent to summarize.]

## Skill Version(s):

1.0.1 (source: release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
