## Description:

SkyDome Taiyi / 天穹-太一 is a portable AI agent operating persona and workbench for planning, evidence-based execution, memory hygiene, workflow management, review, debugging, research, reporting, and practical engineering checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaxia01-1](https://clawhub.ai/user/xiaxia01-1)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent builders use this skill to give an assistant a named operating persona with structured task loops, durable project state, workflow templates, review routines, and helper scripts for diagnostics, API smoke tests, schema inference, prompt evaluation, reports, and release preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill adds a strong persona and workflow layer that may change the assistant's tone, decision style, and task structure.

Mitigation: Install it only when that operating style is desired, and use the quieter/core modes when a minimal assistant posture is needed.

Risk: Helper scripts can create or mutate local state, workflow, report, review, memory, staging, lab, and consolidation files.

Mitigation: Run scripts in a reviewed workspace, inspect paths before execution, and review generated changes before relying on them.

Risk: The staging helper supports a force option that can remove an existing destination.

Mitigation: Use force only after confirming source and destination are separate and the destination is safe to replace.

Risk: The API smoke-test helper sends requests to user-provided URLs.

Mitigation: Avoid untrusted or internal URLs unless the endpoint, headers, data, and network exposure are intentionally approved.

Risk: Self-evolution and review helpers can propose changes that may be incorrect or overbroad.

Mitigation: Treat proposals as review inputs, not automatic changes, and require explicit human review before applying them.

## Reference(s):

- [Taiyi Checklists / 太一清单](references/taiyi-checklists.md)
- [Taiyi Patterns / 太一模式库](references/taiyi-patterns.md)
- [Taiyi Practical Playbooks / 太一实战手册](references/taiyi-practical-playbooks.md)
- [Taiyi Workbench Recipes / 太一实用工作流配方库](references/taiyi-workbench-recipes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text guidance with optional JSON state files, Markdown reports, and Python helper commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local state, workflow, report, review, memory, staging, lab, and dream-consolidation files when the bundled scripts are run.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
