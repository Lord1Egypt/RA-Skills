## Description: <br>
S7 Tap helps agents read Siemens S7 and compatible PLC telemetry over S7comm, including CPU status and DB/M/I/Q values, while keeping data-block writes approval-gated and off by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when an agent needs to inspect Siemens S7 PLC status or read DB, merker, input, and output values by address. It is intended for S7-300/400/1200/1500 and compatible PLC environments where S7comm access is authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Writing to a PLC data block can affect operational technology systems. <br>
Mitigation: Keep dry_run enabled unless the operator has formal authorization, an approved change plan, and a rollback path for the target PLC. <br>
Risk: The skill was previewed against a mocked client rather than live PLCs. <br>
Mitigation: Validate behavior in a controlled non-production environment before using it with production PLCs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline tool parameters, JSON-shaped examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes read-oriented S7 tool selection guidance and guarded write instructions with dry-run behavior.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
