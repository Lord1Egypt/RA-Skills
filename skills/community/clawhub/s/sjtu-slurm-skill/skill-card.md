## Description: <br>
Log in to the SJTU HPC platform as the user to perform job queries, submissions, cancellations, and data management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taleintervenor](https://clawhub.ai/user/taleintervenor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with access to the SJTU HPC platform use this skill to manage HPC account settings, inspect queues and jobs, submit or cancel SLURM work, and move data between storage pools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores HPC tokens, SSH keys, and certificates that can grant access to the user's HPC account. <br>
Mitigation: Install only in a private, trusted workspace and remove or revoke stored tokens, SSH keys, and certificates when they are no longer needed. <br>
Risk: The skill may require an HPC password to request a new token. <br>
Mitigation: Avoid pasting passwords into chat when possible; use the temporary-file flow and delete the file after token issuance. <br>
Risk: Job cancellation, account changes, data deletion, and large transfers can interrupt work or affect user data. <br>
Mitigation: Confirm these operations explicitly with the user before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/taleintervenor/sjtu-slurm-skill) <br>
- [Project homepage](https://github.com/SJTU-HPC/SJTU-SLURM-Skill) <br>
- [SJTU HPC API documentation](https://api.hpc.sjtu.edu.cn/doc/index.html#/) <br>
- [SJTU HPC account security documentation](https://docs.hpc.sjtu.edu.cn/accounts/security.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and command or API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or refresh HPC token, SSH key, and SSH certificate files in a workspace credentials directory.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
