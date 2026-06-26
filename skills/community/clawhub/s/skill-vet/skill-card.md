## Description: <br>
Scans skills before installation or execution for potentially malicious code, suspicious commands, network requests, and other security threats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luwinher](https://clawhub.ai/user/luwinher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Skill Vet before installing or running a skill to scan source files for suspicious JavaScript, shell commands, network access, filesystem operations, and credential-related patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security confidence is limited by the available scanner evidence. <br>
Mitigation: Review the exact skill files and install metadata before installation or execution, and treat scan output as advisory rather than a guarantee of safety. <br>
Risk: Pattern-based vetting can surface suspicious behavior without proving malicious intent. <br>
Mitigation: Manually review reported file paths, line numbers, and snippets before blocking or approving a skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/luwinher/skill-vet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text report with severity-labeled findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings can include scanned file counts, issue counts, severity levels, file paths, line numbers, pattern descriptions, and review guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
