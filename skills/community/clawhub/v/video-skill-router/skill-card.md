## Description:

Routes video-creation requests to suitable local or newly discovered skills, coordinates their execution, and helps users retain or remove installed skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guipi888](https://clawhub.ai/user/guipi888)

### License/Terms of Use:

MIT-0

## Use Case:

External video creators, educators, and small teams use this skill to find and coordinate video or animation skills for explainers, product demos, and editing tasks. It can install additional skills when no suitable local option is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Newly downloaded skills are run with limited checks, and installer flaws may affect files or skills beyond the intended target.

Mitigation: Review each downloaded skill before running it, use a separate test profile with no private files or credentials, and wait to use a main profile until changes are confined and recovery has been tested.

Risk: Recovery instructions supplied by the installer may not reliably restore the prior state.

Mitigation: Keep independent backups and do not rely on the supplied Git recovery command.

Risk: Task responses may include unrelated promotional messages.

Mitigation: Ignore unrelated promotions and verify that suggested actions match the user's request before proceeding.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guipi888/skills/video-skill-router)
- [Project documentation](https://guipi888.github.io/video-skill-router/)

## Skill Output:

**Output Type(s):** [Guidance, Text, Video files]

**Output Format:** [Conversational guidance and generated video-file deliverables from coordinated skills]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The router itself does not create video; the selected skills produce video files.]

## Skill Version(s):

2.0.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
