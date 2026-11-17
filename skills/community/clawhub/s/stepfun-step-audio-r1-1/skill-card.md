## Description:

Use StepFun Chat Completions with model step-audio-r1.1 for non-streaming speech turns that can send text with optional local audio input and save the returned audio, transcript, and raw response object.

This skill is ready for commercial/non-commercial use.

## Publisher:

[praanmichael](https://clawhub.ai/user/praanmichael)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run StepFun step-audio-r1.1 through the Chat Completions API for non-streaming speech interactions. It supports text prompts, optional local audio input, voice selection, and saved response artifacts for review or downstream use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing STEP_API_BASE_URL or passing --api-base-url can send API keys, prompts, and audio to an unintended service.

Mitigation: Use the default StepFun endpoint unless a trusted HTTPS destination has been verified, and prefer a revised release that validates or removes custom API destinations.

Risk: Prompts and local audio are processed by StepFun and may contain sensitive information.

Mitigation: Use only an approved StepFun key and avoid sending sensitive prompts or private audio unless organizational policy permits that processing.

Risk: Voice availability for step-audio-r1.1 can vary by account and may change over time.

Mitigation: Run --list-voices or pass an explicitly approved voice id before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/praanmichael/skills/stepfun-step-audio-r1-1)
- [StepFun Chat API Notes](references/stepfun-chat-api.md)
- [StepFun Voice Selection](references/stepfun-voices.md)
- [StepFun Chat Completion API](https://platform.stepfun.com/docs/zh/api-reference/chat/chat-completion-create)
- [StepFun Chat Object API](https://platform.stepfun.com/docs/zh/api-reference/chat/object)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus generated response files such as JSON, audio, transcript text, and optional content text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls StepFun non-streaming chat completions, can dry-run request JSON, and writes output artifacts to a timestamped or user-selected directory.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
