## Description: <br>
Demand-side client to discover, claim, and deliver RustChain RIP-302 agent jobs based on skills, rewards, and reputation in an escrow marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottcjn](https://clawhub.ai/user/scottcjn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to find suitable RustChain marketplace jobs, reserve them, and submit delivery summaries or URLs. It is suited to agents that need guidance for command-line job discovery, claiming, delivery, reputation lookup, and agent.toml configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub rtc-work listing](https://clawhub.ai/scottcjn/rtc-work) <br>
- [RustChain](https://rustchain.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Security review is clean, but users should review agent.toml, verify the node URL, and avoid combining watch --auto with --yes unless unattended remote job claims are intended.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
