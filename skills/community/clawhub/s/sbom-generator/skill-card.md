## Description: <br>
Generate Software Bill of Materials (SBOM) in CycloneDX or SPDX format for dependency, license, vulnerability, and supply chain inventory needed for compliance and security audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and compliance teams use this skill to inspect project lock files, generate CycloneDX or SPDX SBOMs, and produce license, vulnerability, policy, and diff reports for software releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency and audit commands inspect local repository dependency and lock files, which may expose private project metadata if reports are shared. <br>
Mitigation: Run the skill only in repositories where local dependency inspection is acceptable, and review generated SBOM, license, and vulnerability reports before sharing them. <br>
Risk: Vulnerability audit commands may contact package audit services or use configured private registry authentication. <br>
Mitigation: Review audit commands before execution and run them only in environments approved for private dependency and registry metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/sbom-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and example JSON, CSV, and report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local package audit tools; vulnerability audit commands may use network access or existing registry credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
