## Description:

Helps agent users, skill authors, maintainers, and teams create practical SkillScan-style workflows for bug fixes, setup hardening, reliability improvements, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and agent teams use this skill to turn SkillScan-style security and productivity needs into concrete workflows, checklists, analysis, code changes, or decision support. It is most useful for local-friendly work around bug fixes, setup hardening, reliability improvements, and adjacent skill creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation can activate the skill in unrelated security or bug-fix conversations.

Mitigation: Review implicit invocation before deployment and tighten triggers or disable implicit activation when the skill should only run on explicit requests.

Risk: Advisory outputs can introduce incorrect or misleading workflow guidance if adopted without review.

Mitigation: Validate generated workflows, checklists, code changes, and configuration suggestions against the user's stated success criteria before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-030318)
- [Popular ClawHub skill demand: self-improving agent](https://clawhub.ai/skills/self-improving-agent)
- [Popular ClawHub skill demand: Skill Vetter](https://clawhub.ai/skills/skill-vetter)
- [Popular ClawHub skill demand: SkillScan](https://clawhub.ai/skills/skillscan)
- [Popular ClawHub skill demand: AdMapix](https://clawhub.ai/skills/admapix)
- [Popular ClawHub skill demand: PollyReach](https://clawhub.ai/skills/pollyreach)
- [Ask HN: Are AWS Certs worth getting for experienced Devs?](https://news.ycombinator.com/item?id=48925128)
- [Thinking: Alternate Distribution for Filmmakers](https://news.ycombinator.com/item?id=48931604)
- [Vector search isn't the hard part. Deciding what should be searched is](https://news.ycombinator.com/item?id=48939470)
- [Prototype one playable Zone 1 screen in stylized HD 2D](https://github.com/HiveMind-Crew/hive_mind_rpg/issues/141)
- [Wallpaper Loads Everytime I Go Home](https://github.com/alesimula/Murine-launcher/issues/56)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code, shell command, configuration, checklist, and analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include visible assumptions, limits, validation notes, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
