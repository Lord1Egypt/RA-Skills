## Description: <br>
Guides an agent to call UAPI's GET /image/bing-daily endpoint and handle its image response, optional authentication, quota errors, and documented status codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user explicitly needs Bing's daily wallpaper through UAPI. It helps confirm the endpoint, request shape, authentication posture, response format, and common error handling before calling the API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discovery keywords mention unrelated image capabilities such as compression, base64 conversion, SVG conversion, and NSFW detection. <br>
Mitigation: Use the skill only for retrieving Bing's daily wallpaper through GET /image/bing-daily. <br>
Risk: The endpoint may require a UAPI key or reject anonymous requests after quota limits are reached. <br>
Mitigation: Provide any UAPI key only through normal credential handling, and retry with authenticated access only when the service explicitly requires it. <br>
Risk: Successful responses are image binary data rather than JSON. <br>
Mitigation: Ensure the caller can process JPEG or PNG response bodies before using the endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuakami/uapi-get-image-bing-daily) <br>
- [Quick start](references/quick-start.md) <br>
- [GET /image/bing-daily operation](references/operations/get-image-bing-daily.md) <br>
- [Image resource category](references/resources/Image.md) <br>
- [UAPI base URL](https://uapis.cn/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls] <br>
**Output Format:** [Markdown or concise text instructions with endpoint details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful API responses are image binary data, usually JPEG or PNG, rather than JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
