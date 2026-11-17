## Description:

Publish HTML as a live website instantly. POST HTML, get a shareable URL. No account needed. Always asks the user for confirmation before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snappyio](https://clawhub.ai/user/snappyio)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to publish user-approved HTML, reports, dashboards, documents, landing pages, portfolios, or event pages as public shareable websites through YeetIt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published HTML is publicly accessible and may expose secrets, credentials, private personal data, or proprietary information if the content is not reviewed.

Mitigation: Before approving a publish or update, review the content for secrets, credentials, private personal data, proprietary information, environment values, and other sensitive data.

Risk: A returned edit_key can authorize future changes to a published site.

Mitigation: Keep edit_key values private and share only the public URL with intended viewers.

Risk: Publishing or updating without user awareness can make content public unexpectedly.

Mitigation: Require explicit user confirmation before every publish or update and tell the user the content will be publicly accessible to anyone with the link.

## Reference(s):

- [YeetIt homepage](https://yeetit.site)
- [ClawHub skill page](https://clawhub.ai/snappyio/skills/yeet-it)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl commands, JSON request examples, public URL handling guidance, and confirmation steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and user confirmation before publishing or updating public web content.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
