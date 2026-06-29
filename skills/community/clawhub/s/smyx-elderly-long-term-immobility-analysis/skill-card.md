## Description: <br>
Using fixed cameras in multiple zones of a solo-living elder's home, this skill analyzes video streams for human activity and emits a long-term no-activity alert when activity is not detected within a configured window, defaulting to 12 hours. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, caregivers, elder-care service operators, and developers use this skill to analyze home monitoring video or video URLs for prolonged immobility indicators and to review structured monitoring reports. It is an auxiliary monitoring workflow and should be paired with human confirmation for urgent alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private elder-home video or video URLs may be sent to the provider's cloud service. <br>
Mitigation: Use only with informed consent from the monitored person or authorized family, confirm provider data handling terms, and avoid bathroom or other highly sensitive feeds unless strong privacy controls are in place. <br>
Risk: Reports may be tied to an automatically managed identity and locally or remotely stored tokens. <br>
Mitigation: Review where identity state, reports, and tokens are stored; restrict workspace access; and rotate or remove credentials when the skill is no longer needed. <br>
Risk: A no-activity alert may be wrong or incomplete and does not provide a medical diagnosis or rescue plan. <br>
Mitigation: Treat alerts as prompts for human verification and maintain a separate emergency response process. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-long-term-immobility-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Shared Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON-like structured analysis reports with report links and optional saved text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can list cloud-stored historical monitoring reports and can save the generated report text to a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
