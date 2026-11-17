## Description:

Turns a TikTok creator’s public profile and recent posts, together with supplied collaboration terms, into collaboration brief stills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Media buyers can prepare 4–8 collaboration brief stills for one selected TikTok creator, using the creator’s public profile and recent posts alongside collaboration terms they already wrote. The skill can work from pasted profile details when a TikTok lookup is unavailable, requires separate confirmation before lookup and image-generation stages, and does not post to TikTok.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This still-image skill requests broad Beatra account access shared across packages and reports installation metadata.

Mitigation: Prefer a version with narrower authorization; approve each paid stage, upload only intended assets, and revoke access through the Beatra Console when needed.

Risk: Malformed installation records can cause uninstalling this skill to disconnect other Beatra skills.

Mitigation: Prefer a version with corrected uninstall checks and check other Beatra installations before uninstalling.

## Reference(s):

- [TikTok Creator Brief Stills on ClawHub](https://clawhub.ai/beatra-ai/skills/tiktok-creator-to-brief-stills)
- [Creator lookup](references/creator-lookup.md)
- [Workflow](references/workflow.md)
- [Updates and security](references/updates-and-security.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Images, Text, Markdown]

**Output Format:** [Generated image files plus a labeled Markdown/text lookup memo and still list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usually 4–8 stills (default six); dimensions and destination settings are confirmed for the image stage. Lookup and image generation require separate user approval.]

## Skill Version(s):

0.2.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
