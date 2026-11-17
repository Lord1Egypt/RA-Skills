## Description:

挑选Skill helps users and agents decide which AI Skill is worth installing by providing category picks, search recommendations, similar alternatives, workflow suggestions, and 13-dimension quality analysis across a large skill catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjihua007-rgb](https://clawhub.ai/user/huangjihua007-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to compare candidate AI skills, request recommendations, inspect alternatives, and choose workflow-specific skills before installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends third-party skills and may print direct install URLs, including security or red-team tools.

Mitigation: Verify each recommended skill and installation URL before installing or executing it.

Risk: Development-mode local query logging can occur when a data directory is present.

Mitigation: Remove or monitor artifact/data/search_log.jsonl when running from a development checkout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangjihua007-rgb/skills/tiaoxuan-skill)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [CLI text and markdown-style recommendation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked skill recommendations, comparison notes, workflow picks, install URLs, and quality scores.]

## Skill Version(s):

6.5.0 (source: server release metadata and artifact changelog, released 2026-05-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
