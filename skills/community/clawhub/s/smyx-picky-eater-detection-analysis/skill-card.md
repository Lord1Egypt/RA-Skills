## Description:

Analyzes pet feeding-area videos for selective eating behaviors and provides feeding suggestions and access to past reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and staff at smart-feeder services, boarding centers, or veterinary wards can review feeding-area videos for selective eating, track reported behaviors, and receive feeding suggestions. The skill does not diagnose illness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pet media and identity data are sent to remote services.

Mitigation: Use only media you are comfortable uploading to the provider; request a privacy notice and retention and deletion details before broader deployment.

Risk: The skill may silently create persistent local identity records and store service tokens, particularly in shared workspaces.

Mitigation: Avoid shared workspaces unless you accept local identity and token storage; ask the publisher for scoped authentication before treating the skill as low-risk.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-picky-eater-detection-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [Skill API documentation](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured analysis text or Markdown history table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include report links, behavior summaries, and feeding suggestions.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
