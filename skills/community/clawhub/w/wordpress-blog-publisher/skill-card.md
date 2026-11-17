## Description:

The WordPress Blog Publisher skill helps agents publish, update, and batch-upload blog content to WordPress via the REST API, including authentication, markdown conversion, media uploads, scheduling, and permalink writeback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and publishing teams use this skill to prepare WordPress posts from markdown, upload media, schedule or update posts through the REST API, and record published permalinks back to upstream tracking systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to publish or update live WordPress content while handling WordPress Application Password credentials.

Mitigation: Use HTTPS, create a dedicated least-privilege WordPress account, avoid login passwords, and confirm permissions before publishing.

Risk: Raw markdown, HTML, external images, or embeds may introduce unsafe, broken, or unwanted site content.

Mitigation: Review content and media sources before upload, avoid untrusted markdown, and require explicit review before mirroring external images or raw embeds.

Risk: Batch publishing can propagate a formatting, scheduling, category, tag, or permalink writeback error across many posts.

Mitigation: Run the first post as a dry run or draft, confirm the rendered result, log failures explicitly, and apply rate-limited batch processing.

## Reference(s):

- [WordPress REST API Quick Reference](references/api-reference.md)
- [Markdown to HTML Conversion Rules](references/markdown-to-html-rules.md)
- [WordPress Publishing Quality Checklist](assets/wp-publish-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with REST API request examples, JSON payloads, checklists, and publishing workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WordPress post payloads, media upload instructions, category and tag lookup guidance, scheduling steps, and upstream status writeback patterns.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
