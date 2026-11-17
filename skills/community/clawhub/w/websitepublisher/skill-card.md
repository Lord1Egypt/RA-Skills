## Description:

Build and publish complete websites via WebsitePublisher.ai through conversation, including pages, assets, dynamic data, contact forms, and live URL publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[megberts](https://clawhub.ai/user/megberts)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an OpenClaw agent create, update, and publish WebsitePublisher.ai sites from conversational requests. It supports static pages, uploaded assets, structured dynamic data, and contact forms for live websites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or update live website content in a connected WebsitePublisher.ai project.

Mitigation: Review pages, assets, dynamic records, and contact forms before requesting live changes, and use a separate project when drafting sensitive or unapproved content.

Risk: Secrets, private drafts, or personal data could be exposed through published pages, public MAPI records, or contact forms.

Mitigation: Do not include secrets or private drafts in published content; add privacy or consent language for forms that collect names, emails, or messages.

Risk: The WebsitePublisher.ai API token authorizes changes to the configured project.

Mitigation: Store the token only in trusted agent configuration, avoid sharing it in prompts or page content, and rotate it if exposure is suspected.

## Reference(s):

- [WebsitePublisher.ai](https://www.websitepublisher.ai)
- [WebsitePublisher.ai API Docs](https://www.websitepublisher.ai/docs)
- [WebsitePublisher ClawHub Skill](https://clawhub.ai/megberts/skills/websitepublisher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown with inline JSON, HTML, and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update live website pages, assets, dynamic records, and contact forms through WebsitePublisher.ai APIs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
