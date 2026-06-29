## Description: <br>
Diagnoses likely plant nutrient deficiencies from leaf images or videos and returns structured findings, confidence, and fertilization-direction guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Gardeners, growers, greenhouse operators, and agents supporting plant-care workflows use this skill to analyze leaf images or videos for likely nutrient deficiencies, confidence scores, and next-step guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant images or videos are sent to a remote LifeEmergence service and linked to an automatically managed identity. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid privacy-sensitive media or shared workspaces unless the identity and retention behavior has been reviewed. <br>
Risk: The skill stores tokens locally and can query cloud history with limited user control. <br>
Mitigation: Review local data and token storage before installation, especially on shared machines, and restrict use to trusted environments. <br>
Risk: Visual nutrient diagnosis can be uncertain when symptoms overlap or images are blurry, poorly lit, or incomplete. <br>
Mitigation: Treat results as plant-care guidance rather than a definitive agronomic diagnosis, and confirm with plant context, soil testing, or an agricultural expert before applying treatments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-nutrient-diagnosis-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](artifact/references/api_doc.md) <br>
- [SMYX analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with optional JSON/detail output and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured reports, confidence scores, report links, and cloud history tables.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
