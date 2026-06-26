## Description: <br>
Use when about to claim any work is complete, fixed, passing, or successful - requires running fresh verification commands and reading actual output before making any success claims; evidence before assertions always. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to require fresh verification evidence before reporting that work is complete, fixed, passing, or successful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification commands, builds, tests, or rollback-style regression checks may be expensive or may change local files. <br>
Mitigation: Keep normal command approvals or review enabled in repositories where those checks are costly or could modify local state. <br>
Risk: The skill can delay completion claims because it requires fresh evidence before reporting success. <br>
Mitigation: Run verification commands that are scoped to the claim being made and report the actual command result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/superpowers-verification) <br>
- [Publisher profile](https://clawhub.ai/user/axelhu) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with command and evidence summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no API keys, MCP tools, or credential environment variables were detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
