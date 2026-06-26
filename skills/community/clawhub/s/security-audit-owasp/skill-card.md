## Description: <br>
Full OWASP, Nmap, Nikto vulnerability assessment for OpenClaw deployments. Scan your infrastructure, harden configs, and generate compliance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larios613-hub](https://clawhub.ai/user/larios613-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to plan and run authorized infrastructure security checks, including port scans, web vulnerability scans, OWASP checklist review, and hardening recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Active network scans can affect systems outside the user's authority or expected scope. <br>
Mitigation: Run scans only against infrastructure the user owns or is explicitly authorized to test, and review the target range before execution. <br>
Risk: Generated reports can expose sensitive infrastructure, service, and vulnerability details. <br>
Mitigation: Store audit reports in a controlled location, limit access, and review the output directory before sharing results. <br>
Risk: Automated scans and checklist output are not a complete OWASP or compliance audit. <br>
Mitigation: Use the results as input to a broader manual security review and validate findings before making compliance decisions. <br>


## Reference(s): <br>
- [OWASP Top 10 Audit Checklist](references/owasp-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with bash commands and generated text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include target details and vulnerability findings; treat generated audit output as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
