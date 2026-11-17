## Description:

Log in to the SJTU HPC platform (also known as "交我算") as the user to perform job queries, submissions, cancellations, and data management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taleintervenor](https://clawhub.ai/user/taleintervenor)

### License/Terms of Use:

MIT-0

## Use Case:

External SJTU HPC users use this skill to manage account information, query SLURM jobs and partitions, submit or cancel jobs, and move data between hot and cold storage through HPC APIs and SSH entry nodes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles reusable HPC passwords, bearer tokens, SSH keys, and certificates stored in the workspace.

Mitigation: Use it only in a trusted local environment for an SJTU HPC account the user controls, avoid entering passwords directly in chat, and protect or remove credential files when no longer needed.

Risk: The skill can perform user-level SSH, job, account, and data operations, including actions that may interrupt jobs or affect stored data.

Mitigation: Confirm destructive, account-changing, or job-interrupting actions with the user and verify target partitions, storage paths, and entry nodes before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taleintervenor/skills/sjtu-slurm-skill)
- [Project homepage](https://github.com/SJTU-HPC/SJTU-SLURM-Skill)
- [SJTU HPC API documentation](https://api.hpc.sjtu.edu.cn/doc/index.html#/)
- [SJTU HPC account security documentation](https://docs.hpc.sjtu.edu.cn/accounts/security.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate API calls, SSH sessions, credential setup, and long-running remote job or data operations when used by an agent.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
