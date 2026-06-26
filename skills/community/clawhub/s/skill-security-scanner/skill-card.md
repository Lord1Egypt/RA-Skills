## Description: <br>
Scans OpenClaw skills for security issues, suspicious permissions, and trust scoring before installation or use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Steffano198](https://clawhub.ai/user/Steffano198) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to pre-check OpenClaw skills before installing, auditing, or running untrusted skill bundles. It helps surface suspicious patterns, requested permissions, trust scores, and review recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner can produce reassuring trust scores from shallow pattern checks. <br>
Mitigation: Treat results as a lightweight pre-check and manually review skill files, scripts, requested permissions, and install steps before trusting a safe verdict. <br>
Risk: Shell-based pattern matching can miss obfuscated, indirect, or context-dependent behavior. <br>
Mitigation: Run additional static review and sandbox testing for untrusted skills, especially when scripts, network access, secrets, or package installation are involved. <br>
Risk: The license is not resolved by server evidence for this release. <br>
Mitigation: Confirm the authoritative license terms before redistribution or production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Steffano198/skill-security-scanner) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHavoc security incident](https://www.authmind.com/post/openclaw-malicious-skills-agentic-ai-supply-chain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown reports with trust scores, permission summaries, issue lists, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Trust scores range from 0 to 100 and are accompanied by low, medium, high, or critical risk labels.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
