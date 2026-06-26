## Description: <br>
Security gate for OpenClaw AgentSkills that scans folder and ClawHub skills with cisco-ai-defense/skill-scanner before installation, supports staged installs, and can quarantine high-risk skills via systemd. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-allen-oneal](https://clawhub.ai/user/jason-allen-oneal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to scan OpenClaw skills before installation, review markdown scan reports, and gate or quarantine skills with high or critical findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install gate can fail open when scanning fails or reports cannot be parsed. <br>
Mitigation: Review or patch the scan gate so scanner errors and unparsable reports block installation before relying on it. <br>
Risk: Optional systemd auto-scan creates persistent background monitoring and can move skills into quarantine. <br>
Mitigation: Enable the systemd path unit only when persistent monitoring is intended, and review quarantine behavior and reports after changes. <br>
Risk: External scanner and ClawHub CLI behavior can change over time. <br>
Mitigation: Pin and review the cisco-ai-defense/skill-scanner and ClawHub CLI versions used in the environment. <br>


## Reference(s): <br>
- [Openclaw Skill Scanner on ClawHub](https://clawhub.ai/jason-allen-oneal/skill-scanner-guard) <br>
- [cisco-ai-defense/skill-scanner](https://github.com/cisco-ai-defense/skill-scanner) <br>
- [uv](https://astral.sh/uv) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated markdown scan reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write scan reports, install staged skills, or move high-risk skills into a quarantine directory when its scripts are executed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
