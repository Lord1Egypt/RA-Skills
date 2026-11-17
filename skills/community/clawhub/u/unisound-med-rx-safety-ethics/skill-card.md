## Description:

Answers prescription review, medical safety, and medical ethics or regulations questions using task-specific prompts for question-answer, single-choice, and multiple-choice formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare integrators and developers use this skill to submit prescription review, medical safety, and medical ethics or regulations questions to a configured medical language model. The output is model-assisted information for review workflows, not a substitute for formal clinical decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical answers may be incomplete, incorrect, or unsuitable for a specific patient.

Mitigation: Use outputs as assistive information only and require qualified clinical review before acting on prescription, safety, ethics, or regulations guidance.

Risk: Questions may contain patient data that is sent to the configured model endpoint.

Mitigation: De-identify inputs and use the skill only with a model provider and endpoint approved for the data being processed.

Risk: A caller-supplied API URL can route questions and credentials to an untrusted destination.

Mitigation: Restrict endpoint overrides to trusted HTTPS endpoints under the operator's control.

Risk: Passing API keys directly in shell commands can expose credentials through process listings or shell history.

Mitigation: Use controlled invocation and a safer secret channel instead of embedding keys directly in command lines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-rx-safety-ethics)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Default chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, JSON, files]

**Output Format:** [JSON by default, plain answer text with --text-only, or NDJSON for batch output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write UTF-8 JSON or NDJSON to --output; responses depend on the configured model, endpoint, prompt, and input question.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
