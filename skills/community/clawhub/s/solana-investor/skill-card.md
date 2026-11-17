## Description:

Top-level Solana investment assistant orchestrator that coordinates portfolio, DCA, alerts, and market skills for complex multi-step investment requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liji3597](https://clawhub.ai/user/liji3597)

### License/Terms of Use:


## Use Case:

External users use this skill to coordinate multi-step Solana investment workflows, such as checking portfolio or market state before setting alerts or DCA actions. It is intended for requests that require multiple sub-skills and stepwise confirmation before write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Undocumented operational scripts may expose deployment posture, aggregate application state, configuration, or credential-presence indicators when run with repository and environment access.

Mitigation: Review the package before installing, authorize any script execution explicitly, and run with least-privilege read access only in environments where those scripts are understood.

Risk: The skill coordinates investment-related workflows that can include alerts or DCA setup across sub-skills.

Mitigation: Require stepwise user confirmation for every write operation and keep failed sub-steps isolated from read-only summaries.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text orchestration guidance, with shell command references when delegating to sub-skill scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate read and write workflows across portfolio, market, DCA, and alert skills; write operations require user confirmation.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
