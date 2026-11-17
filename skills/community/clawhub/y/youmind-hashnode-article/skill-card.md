## Description:

Write and publish Hashnode articles through YouMind OpenAPI, with draft-first publishing, post and draft listing, tag lookup, and setup guidance for account readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindy-youmind](https://clawhub.ai/user/mindy-youmind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and content teams use this skill to generate or adapt technical articles for Hashnode, create drafts by default, and publish through a configured YouMind account after user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a YouMind API key to an arbitrary configured API endpoint if base_url is changed.

Mitigation: Use it only with a trusted YouMind API key and keep base_url set to https://youmind.com/openapi/v1 unless intentionally testing a local backend.

Risk: The package contains permanent delete commands that are not shown in the main docs.

Mitigation: Review available CLI commands before deployment and require explicit human approval before any destructive operation.

Risk: Publishing workflows can expose incomplete or inaccurate generated articles.

Mitigation: Prefer draft-first publishing, review the generated Markdown and Hashnode draft, and publish only after user confirmation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mindy-youmind/skills/youmind-hashnode-article)
- [Hashnode API Reference](references/api-reference.md)
- [Hashnode Article Pipeline](references/pipeline.md)
- [Hashnode Platform DNA](references/platform-dna.md)
- [Content Generation Playbook](references/content-generation-playbook.md)
- [Content Adaptation Playbook](references/content-adaptation-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown article drafts, command summaries, result links, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local draft files are expected under output/; publish actions should return draft or post links when available.]

## Skill Version(s):

1.0.0 (source: frontmatter, toolkit package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
