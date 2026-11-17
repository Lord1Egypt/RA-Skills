## Description:

Write and publish WordPress articles end-to-end with AI, including YouMind knowledge-base topic mining, de-AI voice writing, Markdown-to-HTML conversion, featured image upload, and user-approved WordPress publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindy-youmind](https://clawhub.ai/user/mindy-youmind)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a topic or existing Markdown into a WordPress-ready article, preview it locally, and publish or draft it through a WordPress site connected in YouMind.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect a production WordPress site through publishing and broad site-management actions.

Mitigation: Use a least-privilege WordPress account, review drafts before publishing, and avoid delete, comment, or category administration commands unless site administration is intended.

Risk: Unreviewed generated content or untrusted Markdown may publish incorrect material or problematic media references.

Mitigation: Preview locally, review the full draft and image frontmatter, and prefer draft status until the user explicitly approves publication.

Risk: Misconfigured credential routing can send requests to an unintended endpoint.

Mitigation: Keep youmind.base_url on the official HTTPS YouMind endpoint unless intentionally testing, and keep WordPress credentials connected through YouMind rather than local repo files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mindy-youmind/skills/youmind-wordpress-article)
- [YouMind WordPress OpenAPI Reference](references/api-reference.md)
- [Pipeline Overview](references/pipeline.md)
- [WordPress Platform DNA](references/platform-dna.md)
- [Content Generation Playbook](references/content-generation-playbook.md)
- [Content Adaptation Playbook](references/content-adaptation-playbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API Calls, Files]

**Output Format:** [Markdown articles, HTML previews, JSON/API responses, CLI command output, and concise result links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local article draft files and may create or update WordPress posts after user approval.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
