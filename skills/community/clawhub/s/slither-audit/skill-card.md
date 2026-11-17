## Description:

Run slither static analysis on Solidity contracts. Fast, lightweight security scanner for EVM smart contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aviclaw](https://clawhub.ai/user/aviclaw)

### License/Terms of Use:


## Use Case:

Developers and smart contract engineers use this skill to run local Slither analysis against Solidity files or contract directories and generate security findings reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Failed compilation, missing tools, malformed Slither output, or other scan failures may be reported as zero findings.

Mitigation: Confirm Slither completed successfully before trusting a clean report, and run the skill in an isolated environment with a pinned Slither version.

## Reference(s):

- [Slither](https://github.com/crytic/slither)
- [ClawHub Skill Page](https://clawhub.ai/aviclaw/skills/slither-audit)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, guidance]

**Output Format:** [Markdown report or JSON object with vulnerability findings and severities]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Solidity files only; requires valid Solidity code and an installed Slither analyzer.]

## Skill Version(s):

0.4.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
