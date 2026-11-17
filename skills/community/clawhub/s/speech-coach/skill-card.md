## Description:

Speech Coach is a text-based AI public speaking coach with a 15-step curriculum, 25 speaking methods, scenario practice, and local progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chameleon-nexus](https://clawhub.ai/user/chameleon-nexus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill to practice public speaking through text conversation, structured exercises, script annotation, scoring, and milestone-based coaching. It is suited for presentation preparation, impromptu speaking practice, workplace communication, and confidence-building exercises.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves a local user profile and training history under the OpenClaw workspace.

Mitigation: Avoid entering sensitive workplace details that should not be retained, and review or delete the speech-coach workspace files to clear progress.

Risk: Users may expect voice or video assessment from a speaking coach, but this skill is text-only.

Mitigation: Use the script annotation and quiz workflow for in-chat evaluation, and treat offline mirror, recording, or video review as user-managed practice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chameleon-nexus/skills/speech-coach)
- [README.md](artifact/README.md)
- [Curriculum](artifact/curriculum.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown conversation with inline shell commands and local JSON progress records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only coaching; no audio or video processing; stores local profile and progress files under the OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
