## Description: <br>
PwnClaw Security Scan helps test AI agents for security vulnerabilities using PwnClaw attacks and remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gemini2027](https://clawhub.ai/user/Gemini2027) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run or coordinate PwnClaw security scans against an AI agent, review the resulting security score, and apply remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scan prompts and agent responses may be sent to PwnClaw. <br>
Mitigation: Install and use the skill only when that data sharing is acceptable for the agent and test environment. <br>
Risk: Generated remediation rules could be too broad or unsuitable as permanent system instructions. <br>
Mitigation: Review each rule, narrow it to the specific vulnerability, and retest before making it permanent. <br>


## Reference(s): <br>
- [PwnClaw website](https://www.pwnclaw.com) <br>
- [ClawHub skill page](https://clawhub.ai/Gemini2027/pwnclaw-security-scan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with optional HTTP request descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve sending scan prompts and agent responses to PwnClaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
