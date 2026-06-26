## Description: <br>
Analyzes self-hosted SonarQube projects, retrieves filtered issues, checks Quality Gate status, and suggests remediation steps for code-quality findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FelipeOFF](https://clawhub.ai/user/FelipeOFF) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and CI maintainers use this skill to query a configured self-hosted SonarQube instance for project or pull-request issues, generate JSON or Markdown reports, and decide which findings need manual remediation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries a configured SonarQube server and may use a SonarQube token. <br>
Mitigation: Set SONAR_HOST_URL deliberately, prefer HTTPS for remote servers, use a least-privileged token, and keep tokens out of committed configuration, logs, and screenshots. <br>
Risk: The autoFix option is described as an analysis option in this release and suggested fixes may be incomplete or unsuitable. <br>
Mitigation: Treat suggested fixes as review input and manually inspect changes before applying or merging them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FelipeOFF/sonarqube-analyzer) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [openclaw.plugin.json](openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, Markdown, and CLI text with remediation guidance and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured SonarQube server URL, authentication token, and project key.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
