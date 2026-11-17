## Description:

Automates server maintenance by checking disk usage, cleaning caches, optimizing resources, and supporting local and remote multi-server batch operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to inspect disk and memory usage, clean selected caches, and run maintenance across configured local or SSH-accessible servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch maintenance can run root SSH commands against hard-coded public server targets.

Mitigation: Replace all targets with validated hosts, pin SSH host keys, and avoid root access unless it is explicitly required and tightly controlled.

Risk: Cleanup commands can delete cache data without an apply confirmation in batch mode.

Mitigation: Require dry-run review or an explicit confirmation before cleanup, especially on production systems.

Risk: Scheduled execution could repeat unsafe maintenance against the wrong targets.

Mitigation: Enable scheduling only after reviewing the server configuration, access model, and cleanup scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2233admin/skills/server-maintenance)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and tabular maintenance reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports before and after disk usage, cleanup status, and configuration-driven server targets.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
