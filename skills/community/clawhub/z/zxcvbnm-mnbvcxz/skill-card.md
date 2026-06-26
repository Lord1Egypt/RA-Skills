## Description: <br>
Executes AIVideoMaker API workflows for text-to-video and image-to-video generation, including task creation, status polling, task details retrieval, and cancellation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rainlin10](https://clawhub.ai/user/rainlin10) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to create, poll, inspect, and cancel AIVideoMaker video generation tasks from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, image payloads, task IDs, and an AIVideoMaker API key to the AIVideoMaker service. <br>
Mitigation: Install only when the publisher is trusted, provide the API key through environment variables, and review submitted prompts, images, and task IDs before execution. <br>
Risk: Generation and cancellation actions may consume credits or affect an existing video task. <br>
Mitigation: Confirm model, duration, payload, and task ID values before running createGeneration or cancelTask commands. <br>
Risk: Polling can encounter upstream rate limits. <br>
Mitigation: Use the built-in retry and backoff settings, honor Retry-After responses, and keep task query requests within documented service limits. <br>


## Reference(s): <br>
- [AIVideoMaker API Reference](references/api-reference.md) <br>
- [Usage Examples](references/examples.md) <br>
- [AIVideoMaker](https://aivideomaker.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/rainlin10/zxcvbnm-mnbvcxz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON runtime output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime commands return normalized JSON with fields such as ok, status, taskId, data, errorCode, errorMessage, retryAfter, and suggestions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact files report 1.0.12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
