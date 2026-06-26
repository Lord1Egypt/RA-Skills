## Description: <br>
Use when a SOC, MDR, or incident-response analyst needs to triage a single security alert from a SIEM, EDR, XDR, or detection pipeline. Guides structured intake, indicator enrichment, MITRE ATT&CK mapping, and produces a verdict, severity-scored disposition, and audit-ready triage report with recommended next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SOC, MDR, incident-response, MSSP, and detection-engineering analysts use this skill to convert a single SIEM, EDR, XDR, or detection-pipeline alert into a structured triage disposition. It guides intake, IOC extraction, conservative MITRE ATT&CK mapping, severity scoring, verdict selection, and human-confirmed next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alert payloads may contain sensitive usernames, hostnames, IP addresses, file paths, and incident details. <br>
Mitigation: Use the skill only in an agent session approved for sensitive SOC data, and avoid pasting data that is not needed for the triage decision. <br>
Risk: Recommended containment steps such as blocking, isolation, account disablement, or token revocation could disrupt business activity if applied without review. <br>
Mitigation: Treat all containment items as recommendations and require a human analyst to confirm and execute them in the organization's security tools. <br>
Risk: Threat intelligence, IOC reputation, or MITRE ATT&CK mappings may be incomplete when external context is unavailable. <br>
Mitigation: Use only alert payload data and user-supplied enrichment, mark gaps explicitly, and avoid unsupported attribution or technique IDs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/archlab-space/soc-alert-triage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown triage report with tables, verdict, severity rationale, recommended actions, escalation notes, and open questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations only; containment actions and external enrichment require human confirmation outside the skill.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
