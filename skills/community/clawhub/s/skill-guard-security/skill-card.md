## Description: <br>
Security scanner for OpenClaw agent skills that audits skills for dangerous patterns, vulnerable dependencies, and suspicious behavior before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonathanliu811026](https://clawhub.ai/user/jonathanliu811026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub users use this skill to review OpenClaw agent skills before installation and to receive security verdicts and risk breakdowns through CLI or API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The usage examples run npx skillguard-audit, which can download and execute external npm package code. <br>
Mitigation: Confirm the npm package is the intended package, pin a trusted version when possible, and run the audit in a sandbox for higher-risk reviews. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jonathanliu811026/skill-guard-security) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe CLI use, API use, and SAFE/CAUTION/DANGEROUS verdict outputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
