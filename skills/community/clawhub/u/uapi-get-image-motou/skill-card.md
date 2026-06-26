## Description: <br>
This skill helps an agent call UAPI's GET /image/motou endpoint to generate a motou GIF from a QQ number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to prepare or call the UAPI endpoint that generates a motou GIF from a QQ number, including checking the required qq parameter, optional background color, authentication notes, and response codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill metadata includes broad image-processing keywords that do not match the single GET /image/motou endpoint. <br>
Mitigation: Use it only for generating a motou GIF from a QQ number, and do not rely on it for compression, conversion, SVG rendering, or NSFW detection. <br>
Risk: Calls send QQ numbers, and possibly a UAPI key, to the UAPI service. <br>
Mitigation: Provide QQ numbers or credentials only when the user is comfortable sharing them with that service. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/shuakami/uapi-get-image-motou) <br>
- [Quick start](references/quick-start.md) <br>
- [GET /image/motou operation](references/operations/get-image-motou.md) <br>
- [Image resource category](references/resources/Image.md) <br>
- [UAPI base URL](https://uapis.cn/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration] <br>
**Output Format:** [Markdown guidance with endpoint details and parameter checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The successful API response is image/gif binary data; the skill itself provides calling guidance rather than generating the image locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
