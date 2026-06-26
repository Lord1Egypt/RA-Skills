## Description: <br>
SpiderShield Security Scanner provides security scanning and trust scoring for OpenClaw skills, including trust lookup, malware scanning, configuration audit and fixes, rug pull detection, and bulk scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teehooai](https://clawhub.ai/user/teehooai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use SpiderShield to check trust scores for published OpenClaw skills, scan local skill files for malicious patterns, audit and improve OpenClaw configuration, and pin skills to detect later tampering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local shell wrappers and the external spidershield Python package can inspect local skill and OpenClaw configuration files. <br>
Mitigation: Install the Python package from a trusted source, review the command behavior, and run scans in an environment appropriate for security tooling. <br>
Risk: The fix command can modify OpenClaw configuration files. <br>
Mitigation: Run `fix --dry-run` first and review proposed changes before allowing writes. <br>
Risk: The check command contacts the SpiderRating API. <br>
Mitigation: Use it only when sending an author/skill slug to the external service is acceptable under the user's network and privacy policy. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/teehooai/spidershield) <br>
- [SpiderRating Trust Registry](https://spiderrating.com) <br>
- [SpiderShield source repository](https://github.com/teehooai/spidershield) <br>
- [SpiderShield issues](https://github.com/teehooai/spidershield/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text and Markdown-style command output from shell wrappers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The check command sends only an author/skill slug to the SpiderRating API; scan, audit-config, fix, pin, and scan-all operate on local OpenClaw files.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and artifact skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
