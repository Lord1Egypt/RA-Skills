## Description:

Build realtime voice features with Wiro AI, such as live voice conversation, streaming text-to-speech and streaming speech-to-text, by starting a task through the REST API and streaming PCM audio over the Wiro WebSocket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiroai](https://clawhub.ai/user/wiroai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building voice-enabled applications can use this skill to implement live voice conversation, streaming text-to-speech, and live speech-to-text over Wiro's REST and WebSocket APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Microphone audio may be sent to Wiro and the selected model provider.

Mitigation: Give users clear notice and recording controls before recording, and make the audio destination clear.

Risk: The optional install command uses an unpinned package version.

Mitigation: Review the command before running it and pin the package version you intend to install.

Risk: The security scan was partial because two local references could not be resolved.

Mitigation: Resolve and review the referenced files, then run a complete security scan before deployment.

## Reference(s):

- [Wiro AI Realtime Voice skill page](https://clawhub.ai/wiroai/skills/wiro-realtime-voice)
- [Realtime voice conversation docs](https://wiro.ai/docs/realtime-voice-conversation)
- [Realtime text-to-speech docs](https://wiro.ai/docs/realtime-text-to-speech)
- [Realtime speech-to-text docs](https://wiro.ai/docs/realtime-speech-to-text)
- [WebSocket events docs](https://wiro.ai/docs/websocket)
- [Run a model docs](https://wiro.ai/docs/run-a-model)
- [Task cancellation and cleanup docs](https://wiro.ai/docs/tasks)
- [Wiro AI models](https://wiro.ai/models)
- [Wiro AI pricing](https://wiro.ai/product/pricing)
- [Swift-Realtime example app](https://github.com/wiroai/Swift-Realtime)
- [Kotlin-Realtime example app](https://github.com/wiroai/Kotlin-Realtime)
- [Dart-Realtime example app](https://github.com/wiroai/Dart-Realtime)
- [ReactNative-Realtime example app](https://github.com/wiroai/ReactNative-Realtime)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Configuration instructions]

**Output Format:** [Markdown with JSON and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Implementation guidance for REST and WebSocket audio sessions, including example event payloads and PCM framing.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
