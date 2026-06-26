## Description: <br>
Use PoYo AI Z-Image for prompt-based image generation through the PoYo generation API, with simple model, prompt, and size controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to prepare and submit PoYo Z-Image text-to-image requests, choose supported canvas sizes, and capture returned task IDs for status polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, payload contents, and callback URLs are sent to the external PoYo API. <br>
Mitigation: Avoid sensitive data in prompts or callback URLs and review payloads before submission. <br>
Risk: The POYO_API_KEY credential can be exposed if copied into prompts, command history, logs, or shared files. <br>
Mitigation: Keep POYO_API_KEY in a trusted environment variable and avoid embedding the key directly in saved payloads or examples. <br>
Risk: Submitting generation requests may consume PoYo credits. <br>
Mitigation: Confirm the target model, prompt, size, and account context before making API calls. <br>


## Reference(s): <br>
- [PoYo Z Image API Reference](references/api.md) <br>
- [PoYo Z-Image documentation](https://docs.poyo.ai/api-manual/image-series/z-image) <br>
- [PoYo task status documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [PoYo Z-Image OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/z-image.json) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/z-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples and shell commands; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the chosen model id, parameter summary, returned task_id, and next-step polling or webhook guidance when a request is submitted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
