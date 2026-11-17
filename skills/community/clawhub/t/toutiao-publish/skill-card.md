## Description:

Automates publishing Toutiao micro-posts and articles through browser-driven title entry, body injection, image and cover selection, declaration settings, preview, and publish steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axdlee](https://clawhub.ai/user/axdlee)

### License/Terms of Use:

MIT

## Use Case:

External content creators and automation developers use this skill to prepare and publish Toutiao micro-posts or articles from an agent session, including text injection, image recommendations, cover selection, platform declarations, and final publishing.

### Deployment Geography for Use:

Global, subject to Toutiao account availability and applicable platform rules.

## Known Risks and Mitigations:

Risk: The skill can automatically publish content to a real logged-in Toutiao account.

Mitigation: Use only a disposable or intended Toutiao account, stop at draft or preview where possible, and require a human review before final publication.

Risk: The skill uses browser JavaScript injection patterns for article content.

Mitigation: Do not feed it untrusted article HTML or unsanitized generated content; review and sanitize content before injection.

Risk: The release security verdict is suspicious.

Mitigation: Review the skill carefully before installation and run it in an isolated browser profile with access limited to the intended Toutiao workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/axdlee/skills/toutiao-publish)
- [Publisher Profile](https://clawhub.ai/user/axdlee)
- [Publisher GitHub Profile](https://github.com/axdlee)
- [Toutiao Creator Portal](https://mp.toutiao.com)
- [Verified Published Toutiao Article](https://www.toutiao.com/item/7613329346194850310/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline browser automation commands, JavaScript snippets, and shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated Toutiao account and a browser automation environment with current page snapshots.]

## Skill Version(s):

6.1.0 (source: server release metadata and SKILL.md frontmatter; package.json lists 6.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
