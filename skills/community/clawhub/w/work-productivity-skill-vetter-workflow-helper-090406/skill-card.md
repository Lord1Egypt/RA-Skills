## Description:

Helps AI-agent users, skill authors, maintainers, and teams create practical workflows, checklists, analysis, and implementation support for Skill Vetter-style productivity, security, reliability, and adjacent-skill work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users, skill authors, maintainers, and teams use this skill to turn Skill Vetter-style needs into practical workflows, checklists, analysis, code changes, or decision support for bug fixing, setup hardening, safety review, reliability improvement, and adjacent skill creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording and implicit invocation may route unrelated productivity, security, or GitHub work to this helper.

Mitigation: Review or narrow the trigger metadata before installing in environments that rely on automatic skill routing.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Vetter demand signal](https://clawhub.ai/skills/skill-vetter)
- [ClawHub GitHub skill demand signal](https://clawhub.ai/skills/github)
- [ClawHub SkillScan demand signal](https://clawhub.ai/skills/skillscan)
- [Hacker News inference server workflow signal](https://news.ycombinator.com/item?id=49014048)
- [Hacker News publishing workflow signal](https://news.ycombinator.com/item?id=49009663)
- [Hacker News GitHub API workflow signal](https://news.ycombinator.com/item?id=49003232)
- [Qwen Code context provider issue](https://github.com/QwenLM/qwen-code/issues/7585)
- [ngx-print PDF filename issue](https://github.com/ngx-print/ngx-print/issues/331)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code blocks, shell commands, templates, or checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, and follow-up risks when useful]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
