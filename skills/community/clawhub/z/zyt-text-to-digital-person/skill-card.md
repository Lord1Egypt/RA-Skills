## Description: <br>
Use Chanjing text-to-digital-person APIs to create AI portrait images, turn them into talking videos, optionally run LoRA training, poll async tasks, and explicitly download generated assets when requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyuting214](https://clawhub.ai/user/zuoyuting214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to call Chanjing APIs for creating digital-person images, generating talking videos, checking asynchronous task status, optionally running LoRA training, and downloading generated assets only when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Chanjing API credentials and may cache access tokens in a credentials file. <br>
Mitigation: Keep the credentials file permission-restricted, set CHANJING_CONFIG_DIR only yourself, and rotate credentials if they are exposed. <br>
Risk: Generated assets may be downloaded to local storage and API calls may consume paid Chanjing quota or billing. <br>
Mitigation: Download files only after an explicit request, review output locations, and monitor Chanjing quota or billing tied to the credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zuoyuting214/zyt-text-to-digital-person) <br>
- [Chanjing Open API](https://open-api.chanjing.cc) <br>
- [Chanjing OpenAPI login](https://www.chanjing.cc/openapi/login) <br>
- [reference.md](reference.md) <br>
- [examples.md](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, API task identifiers, media URLs, and local file paths when downloads are requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Chanjing credentials and can save generated assets under outputs/text-to-digital-person/ after explicit download requests.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
