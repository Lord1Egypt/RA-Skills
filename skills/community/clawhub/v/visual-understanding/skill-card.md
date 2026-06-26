## Description: <br>
Provides integration guidance for using the Zhipu GLM-4.6V multimodal vision model with local image Base64 uploads, public image URLs, the zai Python SDK, and a cURL fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IsabellaZhangYM](https://clawhub.ai/user/IsabellaZhangYM) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to connect agents or automation workflows to GLM-4.6V for image description, multi-image comparison, and visual information extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected images and prompts to Zhipu/BigModel services. <br>
Mitigation: Avoid submitting confidential, regulated, or personally identifying images unless approved and consistent with the provider's data handling terms. <br>
Risk: API key exposure could allow unauthorized use of the Zhipu/BigModel account. <br>
Mitigation: Keep ZHIPUAI_API_KEY in an environment variable and do not hard-code it in scripts, prompts, or shared files. <br>
Risk: Installing the zai dependency changes the local Python environment. <br>
Mitigation: Prefer an isolated Python environment before installing dependencies for this skill. <br>


## Reference(s): <br>
- [GLM-V project homepage](https://github.com/zai-org/GLM-V) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Python SDK and cURL access patterns and requires ZHIPUAI_API_KEY for API calls.] <br>

## Skill Version(s): <br>
0.0.5 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
