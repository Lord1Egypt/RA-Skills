## Description: <br>
Analyzes 30-60 second adult facial videos or video URLs with cloud rPPG processing to estimate HRV metrics, trend signals, stress/fatigue indicators, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit adult still-face video files or URLs for HRV trend monitoring, historical report lookup, and structured health-trend summaries. The output is intended for personal wellness trend awareness and should not be treated as a medical diagnosis or clinical cardiovascular assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive face video and HRV-related data are sent to the publisher's cloud service. <br>
Mitigation: Use only with informed consent and avoid highly sensitive videos unless the publisher provides clear retention, deletion, encryption, and account-scoping guarantees. <br>
Risk: The skill may create or reuse local identity and authentication state without direct user interaction. <br>
Mitigation: Review local identity and token handling before deployment, and run the skill only in environments where persistent account state is expected and controlled. <br>
Risk: HRV trend outputs could be mistaken for medical diagnosis or clinical cardiovascular assessment. <br>
Mitigation: Present outputs as wellness trend indicators only and route medical concerns to qualified clinical evaluation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-facial-hrv-trend-monitoring-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [Adult facial HRV API documentation](artifact/references/api_doc.md) <br>
- [SMYX analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON structured report with HRV metrics, trend summaries, risk prompts, recommendations, and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud-generated report export links and historical report lists; local or URL video input is accepted by the skill scripts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
