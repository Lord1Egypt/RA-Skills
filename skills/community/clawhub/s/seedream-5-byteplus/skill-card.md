## Description: <br>
Generate images with Seedream 5 through the BytePlus Ark API using a direct API key, then save the returned image locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gamaleldientarek](https://clawhub.ai/user/gamaleldientarek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate Seedream 5 images from text prompts when they have a BytePlus Ark API key. It is useful when the request specifically calls for Seedream, BytePlus Ark, or a Seedream model such as seedream-5-0-260128. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation requests are sent to BytePlus Ark over the network. <br>
Mitigation: Avoid putting confidential or sensitive material in prompts, and use a dedicated BytePlus Ark API key for this skill. <br>
Risk: The script writes the returned image to a local output path. <br>
Mitigation: Confirm the output path before execution, especially when an explicit file path is provided. <br>
Risk: A shared or overly privileged API key could broaden exposure if the runtime environment is compromised. <br>
Mitigation: Use a scoped or dedicated API key and keep it in the environment or approved secret location instead of embedding it in prompts or skill text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gamaleldientarek/seedream-5-byteplus) <br>
- [BytePlus Ark image generation endpoint](https://ark.ap-southeast.bytepluses.com/api/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration] <br>
**Output Format:** [Shell command invocation that writes a local generated image file and prints the saved path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SEEDREAM_API_KEY; SEEDREAM_MODEL and SEEDREAM_SIZE can override the default model and size.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
