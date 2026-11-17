## Description:

Decomposes complex user requests into executable subtasks, identifies required capabilities, searches for existing skills at skills.sh, and creates new skills when no solution exists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[10e9928a](https://clawhub.ai/user/10e9928a)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to break complex, multi-step requests into atomic subtasks, map each subtask to required capabilities, search for existing skills, and plan or create missing skills with user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends unpinned, auto-confirmed global installation of third-party skills.

Mitigation: Pin the Skills CLI and skill revisions, review discovered skill source before use, prefer local or isolated installation, and require explicit approval before adding third-party skills.

Risk: Generated decomposition plans or new skill templates may contain incomplete or incorrect automation guidance.

Mitigation: Review the proposed subtasks, dependencies, generated skill files, and verification steps before executing the plan or installing created skills.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/10e9928a/skills/super-skills)
- [skills.sh](https://skills.sh/)
- [Universal Capability Types Reference](references/capability_types.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with YAML-style task mappings, command examples, skill creation templates, and execution plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed third-party skill install commands and newly drafted skill files; user confirmation is required before skill creation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
