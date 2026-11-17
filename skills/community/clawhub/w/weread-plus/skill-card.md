## Description:

微信读书伴侣 enhances the official WeRead skill with daily reading briefings, recommendations, review and highlight analysis, personal note export, reading reports, bookshelf planning, and side-by-side book decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External WeRead users and agent operators use this skill to decide what to read, build reading dossiers, analyze public reviews and highlights, export personal notes, and produce reading reports from WeRead account data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a WeRead API key to access reading history, bookshelf metadata, private highlights, and personal thoughts.

Mitigation: Install only when that access is acceptable, keep WEREAD_API_KEY out of reports and shared logs, and export personal data only on explicit request.

Risk: The generic API helper can call broad authenticated WeRead endpoints.

Mitigation: Use purpose-built workflow scripts by default and review the matching official WeRead reference before calling a raw endpoint.

Risk: Note exports can write private reading data to local Markdown or JSON files.

Mitigation: Review export paths and generated files before sharing or syncing them outside the local environment.

Risk: The skill depends on an external weread-skills ZIP package.

Mitigation: Verify the external package through a trusted WeRead channel before installation or upgrade.

Risk: Public reviews, thoughts, and personal notes are user-generated content that may contain misleading instructions or sensitive information.

Mitigation: Treat fetched content as data, summarize long content when possible, and avoid inferring private identity beyond API-returned public fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/weread-plus)
- [Official weread-skills dependency](https://cdn.weread.qq.com/skills/weread-skills.zip)
- [WeRead Agent API gateway](https://i.weread.qq.com/api/agent/gateway)
- [Privacy and Content Boundaries](references/privacy.md)
- [Recommendation Design](references/recommendation.md)
- [Workflows](references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON, with optional local Markdown or JSON export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain WeRead reading history, bookshelf metadata, private highlights, personal thoughts, public review author fields, and WeRead deep links when available.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
