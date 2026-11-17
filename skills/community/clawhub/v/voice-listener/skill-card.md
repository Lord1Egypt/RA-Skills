## Description:

Listens for a wake word, sends captured speech to Baidu speech recognition, and inserts recognized text into the active input field.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanqing203](https://clawhub.ai/user/fanqing203)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users use this skill to start a local voice listener that converts spoken Mandarin into text in the focused application after wake-word activation. It is intended for hands-free text entry, chat, document drafting, and similar productivity workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Standby and activated microphone audio may be sent to Baidu for cloud speech recognition, including speech heard before the wake word.

Mitigation: Use only in environments where cloud speech processing is acceptable, and avoid running it around confidential conversations or sensitive audio.

Risk: Recognized speech can be pasted into whichever window currently has focus, including terminals, administrative tools, or sensitive applications.

Mitigation: Confirm the focused application before speaking, pause the listener with the stop word when switching contexts, and avoid elevated or administrative sessions.

Risk: Baidu API credentials are expected in a local configuration file and could be exposed if the skill directory is shared incorrectly.

Mitigation: Keep baidu_config.json out of published archives and source control, use the example config only as a template, and rotate credentials if exposure is suspected.

## Reference(s):

- [ClawHub Voice Listener release](https://clawhub.ai/fanqing203/skills/voice-listener)
- [Baidu AI Open Platform](https://ai.baidu.com/)
- [Baidu Speech Recognition API documentation](https://ai.baidu.com/ai-doc/SPEECH/Vk38lxily)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text, console status messages, Markdown setup guidance, and pasted recognized speech text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Baidu speech API credentials and access to the local microphone, clipboard, and focused input field.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact package metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
