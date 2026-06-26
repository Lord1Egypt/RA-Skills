## Description: <br>
Automates delivery lane scans to detect unresolved blockers, classify failures, update recovery tickets, and attempt bounded recovery actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Delivery operators and automation engineers use this skill to inspect daily delivery lanes, identify blocked or incomplete work, update recovery tickets, and produce diagnosis reports with escalation points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate external publishing and mutate operational state during scheduled or on-demand recovery runs. <br>
Mitigation: Install only in a trusted workspace, review referenced scripts and credentials first, and require human approval before social posts, blog publishing, activation batches, or deployment-affecting commands. <br>
Risk: Recovery actions could repeat failed operations or act with broader access than intended. <br>
Mitigation: Use least-privileged accounts, keep retry caps and escalation rules in place, prefer dry-run testing for new publish paths, and maintain rollback and audit controls. <br>


## Reference(s): <br>
- [Delivery Diagnosis Template](artifact/TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with JSON diagnosis reports, ticket updates, runner logs, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update recovery tickets and operational logs; external publishing and deployment-affecting actions require review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
