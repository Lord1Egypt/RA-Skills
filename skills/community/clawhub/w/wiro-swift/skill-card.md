## Description:

Build iOS and SwiftUI apps with WiroKit, the official Wiro AI Swift SDK, from Swift Package Manager setup and proxy, API key or signature auth to typed and catalog model runs, file uploads, task tracking, cancellation and errors. Use when Swift code needs to generate images, video, music, speech or LLM output with Wiro in an iOS app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiroai](https://clawhub.ai/user/wiroai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build iOS and SwiftUI apps that call Wiro models for image, video, music, speech, and language model tasks, including authentication, uploads, task tracking, and error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial, so some source references were not resolved during scanning.

Mitigation: Review the skill source and its external service connections before installing or using it.

Risk: The optional installation command does not pin a version, so the installed source may change over time.

Mitigation: Review the Wiro-Plugin source and chosen revision before running the installation command.

Risk: Wiro model runs are billed to the user's Wiro project, and blindly resubmitting after a timeout can create a second charge.

Mitigation: Check the task status with its saved task token before resubmitting, and check the model's estimated cost and settings before a run.

## Reference(s):

- [WiroKit Swift Package](https://github.com/wiroai/Swift-QuickStart.git)
- [Wiro documentation: introduction](https://wiro.ai/docs/introduction)
- [Wiro authentication documentation](https://wiro.ai/docs/authentication)
- [Wiro model catalog](https://wiro.ai/models)
- [Wiro pricing](https://wiro.ai/product/pricing)
- [Wiro error reference](https://wiro.ai/docs/error-reference)
- [Wiro realtime voice for iOS](https://github.com/wiroai/Swift-Realtime)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, API calls, Guidance]

**Output Format:** [Markdown with Swift code examples and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
