## Description: <br>
吞贼·净化魄 provides agent guidance for error detection, recovery, redundancy cleanup, fault tolerance, and diagnostic reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lt8899789](https://clawhub.ai/user/lt8899789) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide system health checks, diagnose abnormal behavior, plan recovery actions, and produce remediation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to perform broad cleanup and recovery actions without clear approval or scope limits. <br>
Mitigation: Use it first for read-only diagnostics and require an explicit proposed change list plus user approval before deleting files, restarting processes, triggering garbage collection, rolling back versions, or sharing diagnostic reports from logs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown diagnostic reports with optional command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose recovery, cleanup, rollback, retry, circuit breaker, graceful degradation, and reporting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
