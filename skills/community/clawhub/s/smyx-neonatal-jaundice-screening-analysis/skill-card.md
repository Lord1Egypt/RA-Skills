## Description: <br>
Using a neonatal monitor or baby camera, the system captures high-resolution facial images of the newborn and uses AI visual analysis to detect sclera color and facial skin yellowness to output a low, medium, high, or inconclusive jaundice-risk screening hint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, caregivers, and clinical support teams use this skill to submit newborn facial images or short videos for visual jaundice-risk pre-screening and to retrieve prior screening reports. Outputs are screening hints and follow-up guidance, not medical diagnoses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may transmit newborn images or videos, open-id or phone-like identifiers, and report-history requests to a remote service. <br>
Mitigation: Use only with explicit guardian consent, confirm the remote service is acceptable for the deployment, and avoid submitting unnecessary personal data. <br>
Risk: The skill may keep local account tokens or profile data in a workspace SQLite database. <br>
Mitigation: Restrict workspace access, rotate or remove stored credentials when no longer needed, and review local storage handling before deployment. <br>
Risk: The skill provides non-diagnostic visual screening hints for newborn jaundice. <br>
Mitigation: Treat medium, high, inconclusive, or concerning results as prompts for clinician evaluation and bilirubin measurement rather than as a diagnosis. <br>
Risk: The security summary notes mismatched generic or pet-analysis behavior that may confuse review or operation. <br>
Mitigation: Review configuration and command behavior before release, especially category defaults and any user-facing labels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-neonatal-jaundice-screening-analysis) <br>
- [Neonatal jaundice screening API documentation](references/api_doc.md) <br>
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or Markdown screening reports with risk level, confidence, feature metrics, recommended action, and historical-report tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include low_risk, medium_risk, high_risk, or inconclusive risk labels and caregiver-facing follow-up text.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
