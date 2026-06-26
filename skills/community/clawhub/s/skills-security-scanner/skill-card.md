## Description: <br>
Audits and scans agent skills for potential security issues before they are enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qihuang0](https://clawhub.ai/user/qihuang0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill before installation, audits, or skill development to submit a target skill directory or archive for scanning and summarize returned findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner may package and upload the selected skill directory or archive to the configured scanning endpoint. <br>
Mitigation: Scan only narrow, non-sensitive skill paths and verify the endpoint before execution. <br>
Risk: Scanning can involve API credentials for the configured service. <br>
Mitigation: Use narrowly scoped credentials and avoid pointing the tool at broad workspace, home, or secret-bearing paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qihuang0/skills-security-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Markdown, Guidance] <br>
**Output Format:** [JSON scan results plus a human-readable Chinese Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an absolute path to a skill directory or archive and scanner credentials or endpoint configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
