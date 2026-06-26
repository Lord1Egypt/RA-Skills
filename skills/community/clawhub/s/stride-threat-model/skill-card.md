## Description: <br>
Use this skill when a security engineer, AppSec reviewer, or architect needs to threat-model a system, feature, or architecture change using STRIDE. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, AppSec reviewers, architects, and product security teams use this skill to turn a single system or feature design into a draft STRIDE threat model for design review or pre-launch security review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes architecture and security-design details supplied in chat, which may include sensitive system information. <br>
Mitigation: Avoid pasting real secrets; treat shared component names, hostnames, IPs, and customer identifiers as confidential review inputs. <br>
Risk: Threat-model outputs are advisory and may be incomplete or incorrect when design evidence is missing or ambiguous. <br>
Mitigation: Review the draft with a security architect and resolve open design questions before using it for sign-off. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/stride-threat-model) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with tables and lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft STRIDE report with asset inventory, trust-boundary map, threat table, prioritized top threats, mitigation backlog, and open questions.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata; artifact changelog top entry is 0.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
