## Description:

Use smart journal monitor for evidence insight workflows that need structured execution, explicit assumptions, and clear output boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research teams use this skill to score locally supplied journal article records, identify likely breakthrough papers, and return ranked findings with concise summaries and explicit assumptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged script reads article data from a user-provided JSON file without enforcing path restrictions or validating the input schema.

Mitigation: Provide only intended workspace-local article JSON files and review inputs before execution.

Risk: The release describes journal monitoring, RSS, and AI behavior more broadly than the evidenced script implements.

Mitigation: Treat the skill as a local article-scoring helper unless additional reviewed implementation evidence is supplied.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/smart-journal-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with optional command output and ranked article summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local, reviewable results from provided article JSON; no external network access is evidenced.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
