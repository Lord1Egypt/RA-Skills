## Description:

Helps agent users, skill authors, maintainers, and teams build Skill Vetter-style workflows for bug fixes, setup hardening, safety checks, reliability improvements, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and agent users use this skill to turn broad Skill Vetter-style needs into practical plans, checklists, workflows, code changes, analyses, or validation notes. It is aimed at local-hardware-friendly productivity work around bug fixing, setup hardening, safety, reliability, and adjacent skill creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate too broadly for ordinary security, GitHub, or bug-fix requests.

Mitigation: Confirm that the user's request needs a Skill Vetter-style workflow, artifact, checklist, analysis, or implementation support before relying on the skill.

Risk: Documentation-only workflow guidance can produce proposals that are incomplete or unsuitable for a specific repository, setup, or security context.

Mitigation: Review the generated plan or artifact against the local success criteria, run relevant checks or scans, and keep assumptions and remaining risks visible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-skill-vetter-workflow-helper-100317)
- [Publisher profile](https://clawhub.ai/user/kyro-ma)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: Skill Vetter](https://clawhub.ai/skills/skill-vetter)
- [Popular ClawHub skill demand: Github](https://clawhub.ai/skills/github)
- [Popular ClawHub skill demand: SkillScan](https://clawhub.ai/skills/skillscan)
- [Hacker News signal: New Inference Server for DGX Spark](https://news.ycombinator.com/item?id=49014048)
- [Hacker News signal: AI-orchestrated publishing workflow](https://news.ycombinator.com/item?id=49009663)
- [Hacker News signal: ZaGuu agent negotiation games](https://news.ycombinator.com/item?id=49019165)
- [GitHub issue signal: kana-dojo good first issue](https://github.com/lingdojo/kana-dojo/issues/25825)
- [GitHub issue signal: WivWav production Workspace consumer](https://github.com/NoAccountNeeded-Lab/WivWav/issues/913)
- [GitHub issue signal: agentic workflows React app](https://github.com/lfarci/my-agentic-workflows/issues/7)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code, shell command, checklist, workflow, and validation sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should expose assumptions, limits, success criteria, verification notes, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
