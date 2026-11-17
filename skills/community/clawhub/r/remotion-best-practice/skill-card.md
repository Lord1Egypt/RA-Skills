## Description:

Best practices for Remotion - Video creation in React

This skill is ready for commercial/non-commercial use.

## Publisher:

[start-fish](https://clawhub.ai/user/start-fish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video engineers use this skill when building Remotion projects in React, including composition setup, timeline animation, media handling, captions, audio workflows, fonts, transitions, maps, and render checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned package commands and native download workflows may install unexpected versions.

Mitigation: Review commands before running them, prefer pinned versions and lockfiles, and run Whisper or native download workflows in a constrained project environment.

Risk: API-key examples may lead users to expose credentials if secrets are pasted into chat or committed to code.

Mitigation: Keep API keys in environment variables or a secret manager, and avoid sharing secrets in prompts, logs, or repositories.

Risk: Remote media, data, and asset URLs can affect render reproducibility or privacy.

Mitigation: Approve remote URLs explicitly and prefer local, pinned, or reviewed assets for production renders.

## Reference(s):

- [Remotion useWindowedAudioData documentation](https://www.remotion.dev/docs/use-windowed-audio-data)
- [Remotion visualizeAudio documentation](https://www.remotion.dev/docs/visualize-audio)
- [Remotion captions documentation](https://www.remotion.dev/docs/captions)
- [Remotion install-whisper-cpp transcription documentation](https://www.remotion.dev/docs/install-whisper-cpp/transcribe)
- [Remotion Tailwind documentation](https://www.remotion.dev/docs/tailwind)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with TypeScript, TSX, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes modular rule files for Remotion topics such as media, captions, timing, transitions, fonts, maps, and render validation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
