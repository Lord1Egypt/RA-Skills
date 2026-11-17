## Description:

Test-driven development with red-green-refactor loop and de-sloppify pattern.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huamu668](https://clawhub.ai/user/huamu668)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to plan and implement features or bug fixes with a test-first workflow. It emphasizes behavior-focused tests through public interfaces, incremental red-green-refactor cycles, and a cleanup pass for low-value tests or code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to use an external CLI with broad working-tree scope, which could expose project code or changes outside the user's intended workflow.

Mitigation: Review and explicitly approve any external CLI use, code sharing, or broad working-tree operation before execution.

Risk: The skill includes commit-oriented workflow examples that could create repository history before changes are reviewed.

Mitigation: Require repository-policy review before allowing automated commits, and inspect test, build, and diff output before committing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huamu668/skills/tdd-ecc)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with checklists, examples, and inline code or shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to propose tests, source changes, cleanup steps, verification commands, and commit commands.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
