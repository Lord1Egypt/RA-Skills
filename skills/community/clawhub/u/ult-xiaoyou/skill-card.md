## Description:

Python-based LiveVideoStore client with voice interaction, GUI, volume control, session management, and encrypted audio transmission for live streaming.

This skill is for research and development only.

## Publisher:

[robertlee-lab](https://clawhub.ai/user/robertlee-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers can use this skill to run a Python voice client for live-streaming style interaction, including microphone input, audio playback, session handling, and encrypted audio transport. The artifact states it is for learning and research only and not for commercial use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to external services and sends device and audio data.

Mitigation: Run only in controlled research environments, review the configured endpoints before use, and avoid using it around sensitive conversations.

Risk: Microphone audio may continue transmitting after the user believes push-to-talk recording has stopped.

Mitigation: Test and fix stop-recording behavior before real use, and terminate the process or network connection if recording state is uncertain.

Risk: Connection credentials may be printed to the console.

Mitigation: Do not share console output or logs, and remove credential-printing behavior before broader testing.

Risk: The skill listens for global keyboard events.

Mitigation: Grant keyboard-listener permissions only on systems where that behavior is expected and acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robertlee-lab/skills/ult-xiaoyou)
- [Publisher profile](https://clawhub.ai/user/robertlee-lab)
- [Artifact documentation](artifact/skill.md)
- [Dependency list](artifact/script/requirements.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets plus Python and JSON artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8 or newer, audio input and output devices, network access, and the listed Python dependencies.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
