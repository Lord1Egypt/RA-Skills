## Description:

Drafts and publishes or schedules a post on a Facebook Page (text, link, one or several photos, or a video) through the official Graph API after the user approves the exact post. Use when the user wants to post to their Facebook Page. Facebook Pages only; personal profiles are not supported by the API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT

## Use Case:

People managing Facebook Pages use this skill to prepare, review, publish, or schedule approved posts containing text, a link, photos, or video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared setup guide includes Instagram and Threads instructions that do not apply to Facebook posting.

Mitigation: Follow only the Facebook setup and permission instructions for this task.

Risk: Publishing relies on separate authentication and core skills; those dependencies and live API behavior were not tested.

Mitigation: Review the dependency skills, protect stored tokens, and confirm the Page, content, media, and schedule before approving.

## Reference(s):

- [references/setup.md](references/setup.md)
- [Facebook Pages posts API](https://developers.facebook.com/docs/pages-api/posts)
- [Facebook Page photos API](https://developers.facebook.com/docs/graph-api/reference/page/photos/)

## Skill Output:

**Output Type(s):** [Text, API Calls]

**Output Format:** [Facebook Page post with publication details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The post is published or scheduled only after the user approves its exact content.]

## Skill Version(s):

0.3.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
