## Description:

音色修改、AI翻唱，任务由平台弹性部署调度，支持提交和查询 a7w seedsvc 语音转换任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure an a7w API key, submit source and reference audio URLs to the seedsvc voice-conversion service, and query asynchronous task results. It is intended for users who already have permission to process the input audio and accept the third-party service's billing and availability terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled client can send the user's API key to a configurable host through --host or A7W_HOST.

Mitigation: Use the default https://api.a7w.cn endpoint unless you deliberately trust an alternate endpoint to receive the API key.

Risk: API calls consume the user's a7w account points and repeated asynchronous submissions may create duplicate charges.

Mitigation: Review task parameters before submission, use --no-wait plus task polling when appropriate, and check point usage through the provider account.

Risk: Voice conversion requires audio URLs and may process third-party or personal audio through an external service.

Mitigation: Submit only audio you are authorized to process and review generated outputs for rights, consent, and content compliance before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2253128/skills/sanjianke-seedsvc)
- [Getting started](references/getting-started.md)
- [Submit task API](references/api-submit.md)
- [Query task API](references/api-query.md)
- [General a7w plugin guidance](references/通用说明.md)
- [a7w compute marketplace](https://api.a7w.cn/)
- [AI plugin marketplace](https://aigc.a7w.cn/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local Python standard-library client that submits and polls third-party a7w tasks; results and errors are emitted as JSON.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
