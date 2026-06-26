## Description: <br>
Analyzes images with SiliconFlow's Qwen2.5-VL model to describe scenes, identify objects, and answer image questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomlee2013](https://clawhub.ai/user/tomlee2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send a selected local image and prompt to SiliconFlow Qwen2.5-VL for image description, object identification, scene analysis, and image question answering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images and prompts are sent to SiliconFlow for external processing. <br>
Mitigation: Avoid private screenshots, documents, faces, or regulated content unless external processing is approved. <br>
Risk: API keys can be exposed if typed directly on the command line or stored insecurely. <br>
Mitigation: Prefer an environment variable or secret manager for the SiliconFlow API key and avoid logging command invocations that include secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomlee2013/siliconflow-qwen-vision) <br>
- [SiliconFlow chat completions endpoint](https://api.siliconflow.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, guidance] <br>
**Output Format:** [Plain text response, optionally written to a text file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a caller-provided prompt and image path; model output is capped at 2048 tokens by the bundled script.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
