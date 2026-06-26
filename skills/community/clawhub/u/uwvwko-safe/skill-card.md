## Description: <br>
Browser-safety guidance that helps an agent identify and block high-risk web requests involving secrets, system details, sensitive files, or command execution, then notify the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uwvwko-zzz](https://clawhub.ai/user/uwvwko-zzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to apply conservative browsing-safety checks before acting on webpage content. It is intended to block requests for credentials, sensitive local information, risky file access, or command execution and provide a clear warning with suggested next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is an instruction-only safety layer and should not be treated as a browser or endpoint security product. <br>
Mitigation: Use it as agent guidance alongside normal browser, host, and network security controls. <br>
Risk: Security logs and notifications may contain URLs, prompts, page content, or other sensitive details. <br>
Mitigation: Decide where logs are stored, set retention limits, and redact secrets or sensitive page content wherever possible. <br>
Risk: Conservative blocking rules can produce false positives for legitimate troubleshooting or authorized administrative work. <br>
Mitigation: Require explicit user confirmation for exceptions and prefer sandboxed or read-only environments for risky investigations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown safety warnings and user guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk labels, triggered-rule summaries, recommended actions, and structured security-log examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
