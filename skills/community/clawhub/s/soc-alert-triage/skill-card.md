## Description:

Guides SOC, MDR, and incident-response analysts through structured intake, indicator enrichment, MITRE ATT&CK mapping, severity scoring, and an audit-ready triage report for a single security alert.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

SOC, MDR, incident-response, and detection engineering analysts use this skill to turn a raw SIEM, EDR, XDR, or detection-pipeline alert into a defensible triage disposition, severity assessment, MITRE ATT&CK mapping, and recommended next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SOC alert payloads can contain sensitive hostnames, usernames, IP addresses, and asset identifiers.

Mitigation: Treat alert content as confidential and avoid reusing provided indicators in examples, comparisons, or external lookups.

Risk: Triage recommendations could be mistaken for completed containment or remediation.

Mitigation: Frame blocking, isolation, account disablement, token revocation, and quarantine as recommendations that require confirmation and execution by an authorized human.

Risk: Unsupported enrichment, attribution, or MITRE ATT&CK mapping can mislead incident response decisions.

Mitigation: Use only alert payload data and user-supplied context; mark missing enrichment as unavailable and leave technique IDs blank when evidence is insufficient.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown triage report with tables and action checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces recommendations only; containment, isolation, account disablement, token revocation, and quarantine actions require authorized human execution in security tooling.]

## Skill Version(s):

0.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
