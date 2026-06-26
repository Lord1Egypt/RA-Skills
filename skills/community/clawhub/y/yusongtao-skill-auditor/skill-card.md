## Description: <br>
Audits OpenClaw skills for security risks such as dynamic code execution, system command execution, network operations, file writes, sensitive information patterns, and dangerous imports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yustnust](https://clawhub.ai/user/Yustnust) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to scan OpenClaw skill directories before installation or release and review a summarized report of detected security issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pattern-based scanning may miss context-specific behavior or report false positives. <br>
Mitigation: Use the generated report as a review aid and manually inspect findings before installing, rejecting, or modifying a skill. <br>
Risk: The skill scans local skill directories and depends on the selected path and configured rules. <br>
Mitigation: Run it only against intended skill directories, keep file access read-only where possible, and review custom audit_config.json rules before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Yustnust/yusongtao-skill-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/Yustnust) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Human-readable security audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports total issue counts and groups findings by critical, high, and medium severity.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
