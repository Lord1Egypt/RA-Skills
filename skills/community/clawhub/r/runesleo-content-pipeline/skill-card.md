## Description:

Content Pipeline orchestrates research, angle selection, draft writing, and queue management for creator content workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runesleo](https://clawhub.ai/user/runesleo)

### License/Terms of Use:


## Use Case:

Creators and content developers use this skill to turn a topic, URL, or seed idea into researched drafts and managed queue entries for review, adaptation, approval, and publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad shell and sub-agent capabilities.

Mitigation: Install only in a sandboxed workspace with minimal filesystem and network access, and prefer a version that removes Bash and Agent unless those tools are specifically reviewed.

Risk: Topics, URLs, and fetched web content can contain untrusted or misleading input.

Mitigation: Treat external content as untrusted, avoid internal or private URLs, and verify claims against cited sources before approving drafts.

Risk: The skill can create or update queue and research files in the workspace.

Mitigation: Review changes to content-queue.json and research files before publication or downstream automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runesleo/skills/runesleo-content-pipeline)
- [Publisher profile](https://clawhub.ai/user/runesleo)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown research notes, JSON queue data, and plain-text status or draft responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update content-queue.json and files under research/ in the active workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
