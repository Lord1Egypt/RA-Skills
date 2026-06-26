## Description: <br>
Scans third-party agent skills for malicious code patterns, sensitive-data exposure, unsafe file operations, and network activity before installation or release. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sukimgit](https://clawhub.ai/user/sukimgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, skill users, and administrators use this skill to statically scan Python-based OpenClaw or ClawHub skills for suspicious code, unsafe file access, network activity, and potential secret exposure before installation, publication, or audit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is flagged suspicious because it includes under-disclosed live network probing and firewall-inspection helpers. <br>
Mitigation: Review the code before installation, run it only in a controlled environment, and avoid using network-checking helpers against systems you do not own or have permission to test. <br>
Risk: Scan reports may include snippets, paths, or matched strings from sensitive files. <br>
Mitigation: Scan only intended skill directories and keep generated reports private unless they have been reviewed and redacted. <br>
Risk: Broad scans can traverse personal or unrelated folders and surface data outside the intended review scope. <br>
Mitigation: Pass a specific skill directory as the scan target and avoid running the scanner on home directories, repositories with unrelated secrets, or shared systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sukimgit/skill-security-guard-publish) <br>
- [Publisher profile](https://clawhub.ai/user/sukimgit) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and plain text scan reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include risk scores, risk levels, matched patterns, affected files, and review guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
