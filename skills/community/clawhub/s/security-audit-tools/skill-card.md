## Description: <br>
Security Audit Tools helps agents inspect third-party skills, plugins, repositories, packages, shell installers, and GitHub Actions before download or installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luojin520520](https://clawhub.ai/user/luojin520520) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as an advisory review aid before installing or running third-party code. It guides source reputation checks, package and repository inspection, pattern scanning, and manual review reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence warns that the skill can overstate coverage and that LOW RISK results are only partial indicators. <br>
Mitigation: Treat scan output as advisory, manually review critical files and non-JavaScript assets, and avoid using a LOW RISK score as automatic installation approval. <br>
Risk: Helper scripts may fetch npm metadata, download packages, clone repositories, and persist audit material locally. <br>
Mitigation: Run helper scripts only in an isolated temporary workspace with no secrets, and review downloaded material before trusting or executing it. <br>
Risk: Pattern scanning can miss dynamic behavior, dependency risks, installers, workflows, and logic-level vulnerabilities. <br>
Mitigation: Supplement scanner results with manual review of manifests, workflows, installers, dependencies, and any dynamic execution path. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/luojin520520/security-audit-tools) <br>
- [README](artifact/README.md) <br>
- [Findings Catalog](artifact/findings-catalog.md) <br>
- [Report Template](artifact/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown audit guidance with shell commands and optional JSON scan reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts can create local audit directories and write JSON or text reports for follow-up review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
