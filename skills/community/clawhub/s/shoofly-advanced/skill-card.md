## Description: <br>
Shoofly Advanced adds a pre-execution security check for AI agent tool calls in OpenClaw and Claude Code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wow-leeroy-jenkins05](https://clawhub.ai/user/wow-leeroy-jenkins05) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Shoofly Advanced to review tool calls before execution, block high-risk operations, and log or notify on suspicious tool inputs and results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local checker and notification flow can inspect tool arguments and results. <br>
Mitigation: Install only when the Shoofly binaries and configuration are trusted, and prefer local-only notification channels. <br>
Risk: The skill fails open if the checker is missing, errors, or times out. <br>
Mitigation: Confirm that fail-open behavior is acceptable for the deployment and monitor alert logs for checker failures or timeout warnings. <br>
Risk: Alert and blocked-event logs may contain sensitive tool context. <br>
Mitigation: Verify redaction, access controls, and log retention before using the skill for sensitive work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wow-leeroy-jenkins05/shoofly-advanced) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and curl; may write JSONL alerts and blocked-event logs when configured.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
