## Description:

Creates, schedules, lists, edits, and deletes Typefully drafts, including single posts, threads, and multi-platform posts for X, LinkedIn, Threads, Bluesky, and Mastodon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chapati23](https://clawhub.ai/user/chapati23)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent manage Typefully social media drafts and schedules through the Typefully API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, edit, schedule, publish immediately, and delete social-media drafts through a Typefully API key.

Mitigation: Use a Typefully key scoped to the intended account or social set, protect it as a secret, and supervise delete and publish-now actions.

Risk: The security scan reports a request-construction safety issue for schedule values.

Mitigation: Avoid passing schedule values derived from untrusted text until the JSON construction issue is fixed.

## Reference(s):

- [ClawHub Typefully Skill release page](https://clawhub.ai/chapati23/skills/typefully-drafts)
- [Typefully](https://typefully.com)
- [Typefully API endpoint](https://api.typefully.com/v2)
- [Unix password store](https://www.passwordstore.org/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [JSON API responses and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TYPEFULLY_API_KEY; TYPEFULLY_SOCIAL_SET_ID is optional.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
