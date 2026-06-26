## Description: <br>
Scans files under /workspace/skills for risky code patterns and writes Markdown and JSON security audit reports with install guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tlcyqj2023](https://clawhub.ai/user/tlcyqj2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review local skill files before installation or deployment, identify risky code patterns, and receive advisory remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes audit reports under /workspace, which can create or overwrite report files. <br>
Mitigation: Run it in a workspace where those report paths are acceptable, and review generated reports before relying on their recommendations. <br>
Risk: Risk scores are based on keyword detection and can miss context or produce false positives. <br>
Mitigation: Treat scores as advisory and perform human review for files flagged as medium or higher risk. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, guidance] <br>
**Output Format:** [Markdown and JSON audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports to /workspace and uses advisory keyword-based scoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
