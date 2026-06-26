## Description: <br>
Use this skill when a licensed PT, PTA, or rehab documentation specialist needs to draft an outpatient Physical Therapy Plan of Care aligned to APTA Defensible Documentation and CMS / Medicare Part B requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Licensed physical therapists, supervised PTAs or students, and rehab documentation specialists use this skill to draft outpatient PT plans of care for one patient and one episode of care. It structures PHI-minimized intake, examination summary, ICF problem mapping, measurable goals, interventions, certification details, payer flags, and open questions for licensed PT review and sign-off. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patient identifiers or other PHI could be entered during documentation drafting. <br>
Mitigation: Use initials and age in working drafts, replace direct identifiers with placeholders, and keep PHI within approved clinical systems. <br>
Risk: Drafted content could be mistaken for final clinical documentation or payer determination. <br>
Mitigation: Label output as DRAFT and require licensed PT review, sign-off, and payer-specific verification before clinical use or claim submission. <br>
Risk: Current Medicare, payer, or jurisdiction-specific requirements may differ from the workflow assumptions. <br>
Mitigation: Verify current CMS, payer, and state requirements before relying on certification, KX, threshold, or workers' compensation documentation flags. <br>
Risk: Missing or positive red-flag findings could make a routine plan-of-care draft inappropriate. <br>
Mitigation: Complete the red-flag screen and halt drafting for referral-disposition review when serious symptoms or abuse, neglect, or trafficking concerns are present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/pt-plan-of-care-drafter) <br>
- [Publisher profile](https://clawhub.ai/user/archlab-space) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft plan of care with structured sections and open questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft clinical documentation only; requires licensed PT review and sign-off before clinical use.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and CHANGELOG, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
