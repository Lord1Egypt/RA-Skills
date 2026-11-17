## Description:

This skill helps an agent use UAPI's GET /image/bing-daily endpoint to fetch the current Bing daily wallpaper and understand its response codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill when they need an agent to call the UAPI Bing daily wallpaper endpoint, confirm that no request parameters are required, and handle image responses or documented errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad routing keywords may cause the skill to be invoked for unrelated image tasks.

Mitigation: Use this skill only when the request is specifically about Bing daily wallpaper, and confirm GET /image/bing-daily is the intended endpoint before calling.

Risk: Anonymous use may be rate-limited or may require a UAPI key for some requests.

Mitigation: If the endpoint returns a quota, rate-limit, or authentication error, ask the user to create a UAPI key and retry with that credential.

## Reference(s):

- [Quick Start](references/quick-start.md)
- [Bing Daily Wallpaper Operation](references/operations/get-image-bing-daily.md)
- [Image Resource Reference](references/resources/Image.md)
- [UAPI Base API](https://uapis.cn/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/shuakami/skills/uapi-get-image-bing-daily)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration]

**Output Format:** [Markdown guidance with endpoint details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful endpoint calls return image binary data, usually JPEG or PNG; the skill itself provides guidance rather than storing files.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
