## Description:

Run Wiro AI models from Android and Kotlin apps with WiroKit, the official Wiro SDK for Kotlin and Android, covering Gradle setup, client auth, typed and catalog model runs with coroutines and Flows, file uploads and task control. Use when Kotlin, Android or Jetpack Compose code generates images, video, speech, music or LLM output with Wiro, or when the user mentions WiroKit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiroai](https://clawhub.ai/user/wiroai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Kotlin and Android apps use this skill to integrate WiroKit for model requests, file uploads, task tracking, and task control. It provides implementation guidance for authentication, safe credential handling, billing-aware runs, and recovering task status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration relies on external Wiro API services and may use an optional installer or skill source.

Mitigation: Review and trust the referenced services and source; inspect and pin the installer and skill source before use. Keep long-lived API credentials on a backend proxy for shipped apps, and do not log keys or tokens.

Risk: Security analysis had partial coverage, so some evidence remains incomplete.

Mitigation: Review the skill source and its dependencies before adopting it, especially before running optional installation commands.

## Reference(s):

- [WiroKit Kotlin QuickStart sample](https://github.com/wiroai/Kotlin-QuickStart)
- [Wiro API documentation](https://wiro.ai/docs/introduction)
- [Wiro authentication guide](https://wiro.ai/docs/authentication)
- [Wiro models and pricing](https://wiro.ai/models)
- [Wiro API error reference](https://wiro.ai/docs/error-reference)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown with Kotlin and Gradle code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Implementation guidance for Kotlin and Android integrations]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
