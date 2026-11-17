## Description:

DiGiCo mixer OSC remote control system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zimuge-doudou](https://clawhub.ai/user/zimuge-doudou)

### License/Terms of Use:

MIT-0

## Use Case:

Audio engineers and technical operators use this skill to connect to DiGiCo mixers over OSC, load scenes, adjust channel settings, save snapshots, and check mixer status during rehearsals or live events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: State-changing OSC actions can affect live audio equipment immediately when pointed at a real mixer.

Mitigation: Use the skill only on a trusted, isolated management network with operator confirmation before scene, gain, compressor, or snapshot changes.

Risk: Insufficient endpoint scoping or validation can send commands to unintended mixer targets.

Mitigation: Add target allowlists, real endpoint verification, logging, pinned dependencies, and dry-run behavior before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zimuge-doudou/skills/skill-digico-mixer)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON-compatible action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send state-changing OSC commands to configured mixer endpoints when executed.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
