## Description: <br>
Security scanner for Python skills before publishing to ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johstracke](https://clawhub.ai/user/johstracke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill publishers use this skill to scan Python skill files or directories before publishing, then manually review warnings about dangerous imports, unsafe functions, secrets, and risky file operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner performs basic static pattern matching and may miss context-dependent or obfuscated issues. <br>
Mitigation: Use it as an initial local check, then manually review the skill code and supplement with additional security tools when needed. <br>
Risk: Warnings can include legitimate Python patterns that are not unsafe in context. <br>
Mitigation: Review each warning manually and document why any necessary risky pattern is acceptable before publishing. <br>
Risk: The artifact guidance notes that exit-code behavior should be confirmed before relying on the scanner as an automated publish gate. <br>
Mitigation: Confirm the scanner's behavior in the target workflow and do not treat it as the only publish approval signal. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/johstracke/security-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text console output with warnings and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports line-specific warnings for matched patterns and requires manual interpretation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
