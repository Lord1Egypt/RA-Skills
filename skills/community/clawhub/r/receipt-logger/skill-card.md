## Description: <br>
Receipt Logger describes a workflow for creating append-only audit receipts for agent actions with timestamps, hashes, signatures, and JSON export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuge897](https://clawhub.ai/user/jiuge897) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record agent actions as auditable receipts and export them for later review. Treat the advertised tamper-evident signing behavior as unproven until a complete executable is supplied and tested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill promises runnable, signed receipt logging, but the security evidence says the CLI implementation is missing. <br>
Mitigation: Review before installing or relying on the skill, and do not treat tamper-proof signing claims as proven until a complete implementation is supplied and verified. <br>
Risk: Audit receipts may capture secrets, tokens, personal data, confidential prompts, or regulated information. <br>
Mitigation: Avoid logging sensitive data unless storage, export, access control, and retention protections are clear. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON receipt examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact advertises a receipt-logger CLI, but server security evidence says the executable implementation is missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
