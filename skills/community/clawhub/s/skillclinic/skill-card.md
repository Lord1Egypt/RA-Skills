## Description:

Skill Clinic helps agents diagnose and improve skills, create new skills, run precedent searches, perform release gate checks, and collect operations feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to evaluate existing skills, generate new skill files from requirements, compare similar skills, run release-readiness checks, and capture feedback for later improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose unpinned remote search commands during precedent research.

Mitigation: Confirm remote searches before execution and pin, replace, or review the `npx skills find` command before use.

Risk: Feedback workflows can persist failure context that may include sensitive user or project details.

Mitigation: Make feedback logging opt-in, redact sensitive context before writing records, and define clear deletion rules.

Risk: Creation and optimization workflows may write or edit skill files.

Mitigation: Review generated diffs and run the release gate checks before publishing or relying on modified skills.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fslong520/skills/skillclinic)
- [Theory Reference](reference/theory.md)
- [Skill Quality Criteria](reference/criteria.md)
- [Data Source Guide](reference/data-sources.md)
- [Skill IR Specification](reference/skill-ir.md)
- [From Procedural Skills to Strategy Genes](https://arxiv.org/abs/2604.15097)
- [Skill 101](https://my.feishu.cn/wiki/LWazwBXDUipUZVkYCK2c8JK3nEc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, tables, checklists, generated skill files, shell commands, and JSON or JSONL records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write skill files or feedback records when the user selects creation or feedback workflows.]

## Skill Version(s):

3.0.0 (source: ClawHub release evidence and artifact metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
