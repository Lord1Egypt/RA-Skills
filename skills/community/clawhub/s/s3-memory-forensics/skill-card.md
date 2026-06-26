## Description: <br>
Guides authorized memory acquisition, process analysis, artifact extraction, and incident or malware analysis from RAM captures using Volatility and related tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, incident responders, and forensic practitioners use this skill to plan authorized RAM acquisition and analyze memory dumps for processes, network activity, injection, rootkits, credentials, and extracted artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory acquisition or analysis may be unauthorized or outside the investigator's scope. <br>
Mitigation: Confirm explicit authorization and target scope before running acquisition, inspection, or extraction commands. <br>
Risk: Memory dumps and extracted artifacts may contain passwords, tokens, private activity, and business-sensitive data. <br>
Mitigation: Store dumps and artifacts securely, restrict access, preserve chain of custody, and remove or protect sensitive material before sharing. <br>
Risk: Live acquisition can affect system state or produce incomplete or smeared captures. <br>
Mitigation: Use lightweight acquisition tools, document the time and method, hash captures immediately, and validate findings with multiple sources. <br>


## Reference(s): <br>
- [Volatility 3 symbol tables](https://downloads.volatilityfoundation.org/volatility3/symbols/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with command and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes safety-sensitive forensic commands; requires user authorization and secure handling of memory dumps and extracted artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
