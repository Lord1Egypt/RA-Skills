## Description:

Find fresh, viral Xiaohongshu videos by niche with filters for type, date, and popularity, and extract URLs with valid xsec_token for repurposing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travislius](https://clawhub.ai/user/travislius)

### License/Terms of Use:


## Use Case:

Creators and social media workflow operators use this skill to find recent, popular Xiaohongshu video posts by niche and capture usable source URLs for downstream repurposing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu URLs and share links can include temporary tokens or sharing metadata.

Mitigation: Paste copied URLs only into trusted tools and regenerate fresh links when tokens expire.

Risk: The managed browser may retain a Xiaohongshu login session after the workflow is complete.

Mitigation: Use a separate managed browser profile when session reuse is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travislius/skills/xhs-video-finder)
- [Xiaohongshu](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [guidance, text, shell commands]

**Output Format:** [Markdown with browser workflow commands, filters, troubleshooting notes, and URL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-facing browser workflow guidance; final URLs may contain temporary xsec_token or sharing metadata.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
