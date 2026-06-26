## Description: <br>
Schema for tracking code review outcomes to enable feedback-driven skill improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code review maintainers use this skill to log review findings, verdicts, and rationales in a consistent CSV schema for later quality analysis and skill improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feedback rows can become misleading if they are logged without checking the referenced code and review evidence. <br>
Mitigation: Use the skill's gates to bind each row to repo-relative files, opened line numbers, attributable rule sources, and checkable rationales before appending it. <br>
Risk: Downstream workflows may write CSV rows to an unintended location because this skill only defines the schema and validation guidance. <br>
Mitigation: Have the surrounding workflow explicitly choose and review the target feedback log file before making any file changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anderskev/review-feedback-schema) <br>
- [review-verification-protocol](../review-verification-protocol/SKILL.md) <br>
- [review-skill-improver](../review-skill-improver/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown with CSV schema, tables, and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines a nine-field CSV feedback log schema and validation gates for review outcomes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
