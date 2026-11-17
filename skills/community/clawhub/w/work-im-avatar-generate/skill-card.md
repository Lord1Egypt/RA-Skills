## Description:

AI-powered professional IM avatar generator that turns an uploaded personal photo into a polished business-style headshot and requires a wsdsocial.com API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsd-mj](https://clawhub.ai/user/wsd-mj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and workplace teams use this skill to generate professional IM avatar images from personal photos, with promptable choices for background and outfit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal photos or image URLs to an external avatar-generation API.

Mitigation: Confirm that wsdsocial.com data handling is approved for the use case, use only photos the user has permission to process, and avoid sensitive images unless organizational review permits it.

## Reference(s):

- [Source repository](https://github.com/WSD-MJ/work-im-avatar-generate)
- [ClawHub skill page](https://clawhub.ai/wsd-mj/skills/work-im-avatar-generate)
- [WSD Social skills API key page](https://ai.wsdsocial.com/skills)
- [Work IM Avatar Generate API endpoint](https://ai.wsdsocial.com/api/pub/skills/work-im-avatar-generate/_tool_85)

## Skill Output:

**Output Type(s):** [API Calls, Configuration instructions, Shell commands, JSON]

**Output Format:** [JSON response containing a generated avatar image URL, with Markdown setup and cURL usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WSD_API_KEY and user-provided image URL or base64 image data.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
