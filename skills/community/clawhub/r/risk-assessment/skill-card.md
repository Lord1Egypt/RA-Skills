## Description: <br>
Framework-directable information security risk assessment. Identifies threats, evaluates likelihood/impact via a 3x3 matrix, maps findings to any compliance framework, and recommends risk treatment options with prioritization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dangsllc](https://clawhub.ai/user/dangsllc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security, compliance, and engineering teams use this skill to assess systems or environments, classify assets, identify threats and vulnerabilities, score risks, map findings to an active compliance framework, and prioritize treatment actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Risk findings may be incomplete, mis-scored, or mapped to the wrong framework control if the provided system context is incomplete or inaccurate. <br>
Mitigation: Review the generated risk register with security and compliance stakeholders before using it for formal governance, audit, or remediation decisions. <br>
Risk: The security scan guidance flags sensitive agent authority in maintainer workflows such as moderation commands, GitHub publishing, and full-access review modes. <br>
Mitigation: Install and run the skill only with the intended authority, and use dry-run, confirmation, and no-yolo options where available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dangsllc/risk-assessment) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Guidance] <br>
**Output Format:** [Structured JSON with risk findings, framework mappings, score rationale, an executive summary, and prioritized actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a 3x3 likelihood-impact matrix and recommends remediate, accept, transfer, or avoid treatment options.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
