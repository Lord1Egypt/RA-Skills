## Description: <br>
Wellally Health Skills is a bundle of health-management agent skills for recording user-entered health data, querying records, producing health analyses, tracking risks, and generating reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huifer](https://clawhub.ai/user/huifer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and health-management agents use this bundle to maintain user-entered health records, ask natural-language questions about those records, track condition-specific metrics, receive reference guidance, and create structured summaries or HTML reports. It is for supervised health data management and should not be used for emergencies, diagnoses, medication changes, tapering, or treatment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundle handles sensitive health and medical records with broad local read/write access and persistence. <br>
Mitigation: Install only for a deliberate local health-data assistant use case, minimize stored medical details, supervise file reads and writes, and review generated records regularly. <br>
Risk: Medical-safety boundaries are inconsistent across the artifact, and generated guidance could be mistaken for professional care. <br>
Mitigation: Treat outputs as reference information only; do not rely on the skill for emergencies, diagnosis, treatment decisions, medication changes, or tapering. <br>
Risk: Generated HTML reports and exported summaries may contain sensitive personal health information. <br>
Mitigation: Store exported reports securely, avoid unnecessary sharing, and treat report files as sensitive health documents. <br>
Risk: Medication, interaction, polypharmacy, pregnancy, and mental-health workflows can involve high-consequence decisions. <br>
Mitigation: Require clinician or qualified professional review before acting on medication, pregnancy, crisis, psychological, or treatment-related outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huifer/wellally-health-skills) <br>
- [WellallyHealth partner feature list](artifact/docs/feature-list-for-partners.md) <br>
- [Claude skills documentation snapshot](artifact/skills.md) <br>
- [WHO International Travel and Health](https://www.who.int/ith) <br>
- [CDC Travelers' Health](https://www.cdc.gov/travel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, guidance, configuration] <br>
**Output Format:** [Markdown and structured JSON, with optional HTML health reports and file path confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes local health-data JSON files; some skills generate persisted reports or conversation history.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
