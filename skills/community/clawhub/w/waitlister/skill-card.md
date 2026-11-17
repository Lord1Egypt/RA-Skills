## Description:

Helps agents create and manage product-launch waitlists, hosted landing pages, signups, referrals, statistics, and subscriber tags with Waitlister.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilpr](https://clawhub.ai/user/ilpr)

### License/Terms of Use:

MIT-0

## Use Case:

Founders, marketers, and developers use this skill to launch signup pages, collect and manage subscribers, and monitor waitlist activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing a landing page makes its content publicly accessible.

Mitigation: Review the page content and confirm publication with the user before publishing.

Risk: AI-generated pages consume Waitlister credits.

Mitigation: Check the available credits and obtain approval before generating a page; do not automatically retry.

Risk: Signup and subscriber actions add or modify personal contact records.

Mitigation: Use a dedicated API key and confirm the email address before any verification signup.

## Reference(s):

- [Waitlister skill on ClawHub](https://clawhub.ai/ilpr/skills/waitlister)
- [Waitlister API specification](https://waitlister.me/openapi.json)
- [Waitlister documentation](https://waitlister.me/docs/overview)
- [Waitlister plans and limits](https://waitlister.me/pricing.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with API request examples and results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hosted page links, signup counts, and subscriber details.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
