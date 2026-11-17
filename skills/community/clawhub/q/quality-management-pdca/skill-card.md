## Description:

PDCA+ISO9001质量管理决策系统技能 - 基于PDCA循环和ISO9001质量体系的AI决策质量管控技能，实现任务全生命周期管理、标准化流程、持续改进

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongjie666888](https://clawhub.ai/user/yongjie666888)

### License/Terms of Use:

MIT-0

## Use Case:

Quality teams, project leads, and developers use this skill to structure PDCA workflows, validate ISO9001-aligned checkpoints, evaluate decision quality, manage knowledge records, and generate quality reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe local rule evaluation could execute or apply untrusted rule conditions.

Mitigation: Review rule conditions before installation, keep execution in a contained workspace, and do not let untrusted users control rule conditions.

Risk: Broad file-writing paths could overwrite files or place generated records in unintended locations.

Mitigation: Restrict project IDs and report filenames to trusted values and review generated paths before use.

Risk: Generated reports and knowledge-base records may contain sensitive business information.

Mitigation: Handle generated outputs as confidential records and avoid importing untrusted project data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yongjie666888/skills/quality-management-pdca)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Self-Improving integration notes](artifact/docs/Self-Improving对接说明.md)
- [Development integration notes](artifact/docs/开发方案对接说明.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, Python code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate quality reports and knowledge records that should be treated as sensitive business data.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
