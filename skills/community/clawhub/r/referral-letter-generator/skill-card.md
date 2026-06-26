## Description: <br>
Generate medical referral letters with patient summary, reason for referral. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare providers and clinical operations staff use this skill to generate structured referral letters for specialist consultations, transfers of care, urgent referrals, and routine consultations from validated patient and provider data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install document-generation dependencies at runtime. <br>
Mitigation: Preinstall and pin dependencies in a controlled environment, review them before use, and run the skill in an isolated workspace. <br>
Risk: The skill handles patient information and may write PHI-bearing output files to the workspace. <br>
Mitigation: Use real patient data only under approved local storage, secure transmission, retention, and deletion procedures. <br>
Risk: Generated medical referral content may be incomplete, inaccurate, or unsuitable for clinical use without review. <br>
Mitigation: Require clinician review of the generated letter and verify recipient authorization before transmission. <br>


## Reference(s): <br>
- [Input Template](artifact/references/input_template.json) <br>
- [Quick Reference](artifact/references/quick_ref.md) <br>
- [Medical Referral Letter Standards and Guidelines](artifact/references/referral_standards.md) <br>
- [Medical Referral Letter Templates](artifact/references/templates.md) <br>
- [Clean Referral Template](artifact/references/referral_template_clean.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Referral letter files in PDF, DOCX, HTML, or TXT, with Markdown guidance and shell commands for agent workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires structured patient, referring provider, receiving provider, referral reason, and diagnosis fields; optional urgency, history, medications, allergies, vital signs, lab results, and notes can be included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
