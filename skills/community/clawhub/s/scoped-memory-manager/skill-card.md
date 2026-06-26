## Description: <br>
Installs and manages Scope-Based Memory and Automated REM Sleep (memory consolidation) for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[john-20-ux](https://clawhub.ai/user/john-20-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent maintainers use this skill to replace a bloated global MEMORY.md with scoped topic files and a scheduled memory-consolidation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A scheduled background memory job may rewrite or prune MEMORY.md and topic files without sufficient review. <br>
Mitigation: Require human review before pruning or rewriting memory, scope the files the job may read or modify, and keep backups of MEMORY.md and memory/topics/*.md. <br>
Risk: Users may enable recurring automated memory maintenance without a clear rollback path. <br>
Mitigation: Document how to disable the cron job before installation and verify the schedule is intentional before enabling it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup guidance for memory directories and a cron payload for recurring consolidation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
