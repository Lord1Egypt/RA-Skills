## Description: <br>
Build a private symptom tracker for logging health patterns and preparing for doctor visits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to log symptoms, medications, patterns, and doctor-visit notes in a local workspace while avoiding diagnosis or treatment recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive symptom, medication, and doctor-prep notes locally under ~/symptoms/. <br>
Mitigation: Use device account security, consider disk encryption, and review local backup or sync behavior before logging sensitive health information. <br>
Risk: Doctor-prep summaries may contain sensitive health details that users could share externally. <br>
Mitigation: Review and redact summaries before sharing them with clinicians, caregivers, or other recipients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/symptoms) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown notes and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local notes under ~/symptoms/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
