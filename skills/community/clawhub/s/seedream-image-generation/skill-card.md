## Description: <br>
Image generation via Volcengine Seedream API. Use this when you need to perform Text-to-Image (T2I), Image-to-Image (I2I), or general visual creative tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp7553479](https://clawhub.ai/user/cp7553479) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Volcengine Seedream models for text-to-image, image-to-image, and creative visual generation workflows. It can return API response data and optionally save generated images locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected source images, and request metadata are sent to the configured Seedream endpoint. <br>
Mitigation: Use the trusted official endpoint unless there is a reviewed reason to configure another endpoint, and avoid submitting sensitive prompts or local images. <br>
Risk: A configured endpoint receives the API key used for authorization. <br>
Mitigation: Use a limited API key, keep SEEDREAM_BASE_URL unset or pointed only at a trusted endpoint, and rotate credentials if endpoint trust changes. <br>
Risk: Console logs and returned results can contain prompts, file paths, and generated output metadata. <br>
Mitigation: Treat logs and saved responses as potentially sensitive, and avoid sharing them outside the intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp7553479/seedream-image-generation) <br>
- [Volcengine image generation API documentation](https://www.volcengine.com/docs/82379/1541523?lang=zh) <br>
- [Volcengine Seedream model documentation](https://www.volcengine.com/docs/82379/1330310?lang=zh#36969059) <br>
- [Default Volcengine Ark image generations endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [JSON API responses, shell command examples, and optional downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SEEDREAM_API_KEY; SEEDREAM_BASE_URL can redirect requests to a configured endpoint.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
