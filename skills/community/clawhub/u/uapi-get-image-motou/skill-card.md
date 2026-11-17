## Description:

This skill helps an agent use UAPI's GET /image/motou endpoint to generate a motou GIF from a QQ number with an optional background color.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to prepare or call the UAPI motou GIF endpoint for a specific QQ number, including checking required query parameters and response codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes broad keywords such as compression, base64 conversion, SVG conversion, and NSFW detection that are outside the documented endpoint.

Mitigation: Use the skill only for GET /image/motou, confirm the required qq parameter, and ignore or remove unrelated dispatch keywords.

Risk: The endpoint sends a QQ number to the third-party UAPI service and may be subject to anonymous quota or rate limits.

Mitigation: Confirm the user intends to use the external service and add a UAPI Key only when authentication or quota errors require it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuakami/skills/uapi-get-image-motou)
- [Quick start](references/quick-start.md)
- [GET /image/motou operation reference](references/operations/get-image-motou.md)
- [Image resource reference](references/resources/Image.md)
- [UAPI service](https://uapis.cn)

## Skill Output:

**Output Type(s):** [guidance, configuration, API call]

**Output Format:** [Markdown guidance with endpoint, query parameters, authentication notes, and response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in an external GET request that returns image/gif binary data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
