## Description:

Automates authenticated browser access to a rural cloud platform to look up villager records, extract results, export data, and log out.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rookcat](https://clawhub.ai/user/rookcat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers or operators with explicit authorization use this skill to automate lookup and export of villager records from a rural cloud platform. Because it handles personal records through authenticated browser automation, it should be used only under approved access and data-handling controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates authenticated lookup of personal villager records while its purpose and authorized-use boundaries are unclear.

Mitigation: Require publisher clarification and use only with explicit permission for the target platform and data subjects or records covered by the workflow.

Risk: The artifact describes caching, logging, screenshots, temporary storage, and data export behavior for sensitive records.

Mitigation: Confirm the exact data lifecycle, cache and log contents, screenshot behavior, export location, retention period, and cleanup guarantees before installation.

Risk: The skill depends on browser automation and unpinned or broad runtime dependencies.

Mitigation: Run in a managed isolated environment, pin and review dependencies, and avoid shared machines until the dependency and cleanup posture is confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rookcat/skills/rural-cloud-platform)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact manifest](artifact/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe browser automation, authenticated queries, logging, temporary storage, and export behavior.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
