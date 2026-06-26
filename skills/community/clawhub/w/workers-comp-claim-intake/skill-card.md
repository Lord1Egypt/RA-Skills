## Description: <br>
Guides HR managers, safety officers, employer representatives, and workers' compensation coordinators through workplace injury claim intake, OSHA recordability review, state FROI data collection and deadline flags, and draft FROI and incident investigation report preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR managers, safety officers, employer representatives, and workers' compensation coordinators use this skill to collect workplace injury facts, draft a state-structured First Report of Injury, and prepare an incident investigation report for authorized review before filing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workers' compensation intake may involve sensitive employee health information or personal identifiers. <br>
Mitigation: Use placeholders or pseudonyms where possible, avoid unnecessary SSNs, full dates of birth, and detailed medical records, and store or transmit drafts only through authorized secure channels. <br>
Risk: OSHA recordability, state FROI deadlines, and workers' compensation requirements can be jurisdiction-specific and may require qualified review. <br>
Mitigation: Treat generated determinations and deadlines as preliminary drafts, then verify them with qualified HR, safety personnel, the carrier, TPA, or state workers' compensation board before filing. <br>
Risk: Contractor status and compensability questions can require legal or carrier judgment. <br>
Mitigation: Flag contractor classification and compensability issues for legal, carrier, or authorized employer review before relying on the draft. <br>


## Reference(s): <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft documents with structured sections, sensitive-field flags, deadline reminders, and review blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces two draft documents: a First Report of Injury draft and an incident investigation report for HR and safety officer review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and CHANGELOG, released 2026-05-30) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
