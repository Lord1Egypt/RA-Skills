## Description: <br>
Detect prompt injection, jailbreak, role-hijack, and system extraction attempts. Applies multi-layer defense with semantic analysis and penalty scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to screen user input and tool output for prompt injection, jailbreak, role hijack, system extraction, multilingual evasion, memory persistence, and credential exfiltration attempts before agent logic proceeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad control over agent behavior, including pre-execution checks and lockdown behavior. <br>
Mitigation: Require human approval before enabling lockdown, tool disabling, or sensitive-file monitoring behavior, and review the configuration before deployment. <br>
Risk: The optional installer downloads files from a mutable GitHub main branch. <br>
Mitigation: Prefer ClawHub or manual installation from reviewed artifacts, and avoid running install.sh unless the downloaded content has been inspected. <br>
Risk: Audit logging and outbound alerting can expose sensitive prompt, tool, or incident details. <br>
Mitigation: Keep webhook, translation API, and threat-feed features disabled unless needed, and redact or limit audit logs before storing or forwarding them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/georges91560/security-sentinel-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/georges91560) <br>
- [README](README.md) <br>
- [Security Policy and Transparency](SECURITY.md) <br>
- [Configuration Guide](CONFIGURATION.md) <br>
- [Blacklist Patterns](blacklist-patterns.md) <br>
- [Semantic Scoring](semantic-scoring.md) <br>
- [Multilingual Evasion](multilingual-evasion.md) <br>
- [Advanced Threats 2026](advanced-threats-2026.md) <br>
- [Memory Persistence Attacks](memory-persistence-attacks.md) <br>
- [Credential Exfiltration Defense](credential-exfiltration-defense.md) <br>
- [Advanced Jailbreak Techniques](advanced-jailbreak-techniques.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON status examples, code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes allow/block decision examples, scoring thresholds, logging guidance, and optional alerting configuration.] <br>

## Skill Version(s): <br>
2.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
