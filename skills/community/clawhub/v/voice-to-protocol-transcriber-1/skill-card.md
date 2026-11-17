## Description:

Records experiment steps, observations, and notes into structured protocol files from an interactive local logger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and lab teams can use this skill to capture experiment procedures, observations, and notes as timestamped protocol files during lab work. Reviewers should treat it as a text-based protocol logger because server security evidence says the voice-transcription claims do not match the code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release claims voice transcription, but server security evidence says the code behaves as a text-based protocol logger.

Mitigation: Do not rely on it for voice capture without separate functional review and testing.

Risk: The skill writes experiment records to a configurable local directory.

Mitigation: Choose a trusted save directory and avoid untrusted experiment names or paths.

Risk: The security guidance flags dependency cleanup before installation.

Mitigation: Review and clean requirements before running pip install in an isolated environment.

Risk: Experiment records may contain sensitive clinical, research, or proprietary information.

Mitigation: Use a retention plan before recording sensitive details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/voice-to-protocol-transcriber-1)
- [ClawHub publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown, JSON, or plain text protocol files with timestamped entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local experiment records to a configured save directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
