## Description: <br>
Skill Scorer evaluates SKILL.md files or skill folders against an eight-dimension rubric and returns a bilingual quality report with scores, findings, and actionable improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to review, score, and improve SKILL.md files or complete skill folders before publishing or deploying them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill files submitted for review may contain secrets or sensitive implementation details. <br>
Mitigation: Do not include secrets in skills you ask it to review, and inspect linked content before providing it. <br>
Risk: Generated fixes, rewrites, or optimization suggestions could alter skill behavior in unintended ways. <br>
Mitigation: Review any generated change before applying or publishing it. <br>


## Reference(s): <br>
- [Rubric](references/rubric.md) <br>
- [Report Template](references/report-template.md) <br>
- [Anti-Patterns](references/anti-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Bilingual Markdown quality report with score tables, issue lists, before/after examples, and an optimization roadmap.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese report first, English report second; scores are weighted across 8 dimensions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
