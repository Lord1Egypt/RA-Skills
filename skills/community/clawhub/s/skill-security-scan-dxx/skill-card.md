## Description: <br>
Scan installed OpenClaw skills for potential security risks, including dangerous commands, sensitive path access, and other security issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntaffffff](https://clawhub.ai/user/ntaffffff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to run a local scan over installed OpenClaw skills and identify potentially risky patterns before trusting or deploying them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads installed OpenClaw skill files and may print local file paths or matched snippets in terminal output. <br>
Mitigation: Run it intentionally in a trusted terminal and review output before sharing logs outside the local environment. <br>
Risk: Pattern-based scanning can miss risky behavior or flag benign code as suspicious. <br>
Mitigation: Use scan results as triage input and manually review flagged skills before deployment or trust decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ntaffffff/skill-security-scan-dxx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text terminal report with issue counts and matching file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scans local OpenClaw skill files under ~/.openclaw/workspace/skills by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
