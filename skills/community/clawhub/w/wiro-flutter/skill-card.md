## Description:

Build Flutter and Dart apps on the official Wiro AI SDK (the wiro package on pub.dev) to generate images, video, speech, music and LLM output with typed or generic model requests, file inputs, task tracking and typed results. Use when the user wants AI generation in a Flutter or Dart app through Wiro, or mentions package:wiro, Wiro or a Wiro API key in Dart code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiroai](https://clawhub.ai/user/wiroai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Wiro AI model generation to Flutter apps, Dart servers, and command-line tools. It guides them through model requests, inputs and outputs, task tracking, and safe credential and cost handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested installer uses an unpinned package and repository reference, creating a supply-chain risk; the security evidence is incomplete.

Mitigation: Review the installer and repository and pin dependencies to a trusted immutable version or commit before installation.

Risk: Long-lived Wiro credentials in distributed mobile, web, or desktop builds may be exposed.

Mitigation: Keep credentials on a backend and use the proxied client for production apps; never commit, log, or ship secrets in a client binary.

Risk: Paid model runs can incur duplicate charges if a timed-out or disconnected run is submitted again while still running.

Mitigation: Check the existing task or Wiro dashboard before retrying, and tell the user the model, settings, and expected cost before paid runs.

## Reference(s):

- [Wiro AI documentation](https://wiro.ai/docs/introduction)
- [Wiro AI model catalog](https://wiro.ai/models)
- [Wiro AI pricing](https://wiro.ai/product/pricing)
- [LLM chat streaming guide](https://wiro.ai/docs/llm-chat-streaming)
- [Wiro AI error reference](https://wiro.ai/docs/error-reference)
- [Wiro Dart SDK source and examples](https://github.com/wiroai/Dart-QuickStart)

## Skill Output:

**Output Type(s):** [Dart code, Configuration guidance, API request guidance]

**Output Format:** [Markdown guidance with Dart code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes typed and generic model request examples, file input guidance, task tracking, and credential and cost handling guidance.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
