## Description: <br>
Scan ClawHub skills for security vulnerabilities BEFORE installing. Use when installing new skills from ClawHub to detect prompt injections, malware payloads, hardcoded secrets, and other threats. Wraps clawhub install with mcp-scan pre-flight checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jamesOuttake](https://clawhub.ai/user/jamesOuttake) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and ClawHub users use skill-guard to stage and scan ClawHub skills with mcp-scan before installing them, blocking or quarantining skills when issues are detected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs shell commands that stage, scan, and install other skills. <br>
Mitigation: Review scripts/safe-install.sh before use and install only if you are comfortable with those local actions. <br>
Risk: Force installing can replace an existing skill. <br>
Mitigation: Use --force only when intentionally replacing an existing installation. <br>
Risk: The scan can be skipped by command-line option. <br>
Mitigation: Avoid --skip-scan for normal installs so the pre-install security check runs. <br>


## Reference(s): <br>
- [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce exit codes and quarantined staging paths when threats or errors are found.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
