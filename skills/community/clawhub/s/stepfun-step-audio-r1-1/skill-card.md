## Description: <br>
Use StepFun Chat Completions with model step-audio-r1.1 for non-streaming speech turns that can send text with optional local audio input and save the returned audio, transcript, and raw response object. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[praanmichael](https://clawhub.ai/user/praanmichael) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run StepFun step-audio-r1.1 audio-chat turns through the non-streaming Chat Completions API, optionally sending a local audio file and returning saved audio, transcript, content, and response JSON paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts, system instructions, and local audio files are sent to StepFun under the user's API key. <br>
Mitigation: Use the skill only for content that can be shared with StepFun, and avoid sending sensitive audio or instructions unless approved for that account and use case. <br>
Risk: Saved transcripts, audio files, request JSON, and response JSON may contain sensitive content. <br>
Mitigation: Write outputs to a private directory, restrict access to saved files, and delete generated artifacts when they are no longer needed. <br>
Risk: Overriding the StepFun API base URL can send requests and credentials to an unintended endpoint. <br>
Mitigation: Keep the default StepFun endpoint unless the replacement endpoint is trusted and approved. <br>


## Reference(s): <br>
- [StepFun Chat API Notes](references/stepfun-chat-api.md) <br>
- [StepFun Voice Selection](references/stepfun-voices.md) <br>
- [StepFun chat completion create API](https://platform.stepfun.com/docs/zh/api-reference/chat/chat-completion-create) <br>
- [StepFun chat completion object API](https://platform.stepfun.com/docs/zh/api-reference/chat/object) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files, Text, JSON] <br>
**Output Format:** [Markdown guidance with bash commands, saved audio files, transcript text, and response JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a StepFun API key; local outputs may include response audio, transcript, assistant content, response JSON, and dry-run request JSON.] <br>

## Skill Version(s): <br>
0.1.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
