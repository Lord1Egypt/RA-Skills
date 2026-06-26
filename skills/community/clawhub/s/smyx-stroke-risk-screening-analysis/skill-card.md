## Description: <br>
Analyzes face images or video plus optional physiological indicators to request stroke-risk screening reports with risk levels, warnings, lifestyle suggestions, and medical guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and health-oriented agents use this skill to submit face media and optional blood pressure, blood sugar, or blood lipid indicators for stroke-risk screening and report retrieval. The result is screening guidance only and is not a substitute for professional medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends face images or videos, physiological indicators, and a user identifier to configured Life Emergence remote APIs. <br>
Mitigation: Use the skill only after confirming the service privacy terms, data handling expectations, and that users consent to transmitting biometric and health-related data. <br>
Risk: Local identity or token data may be stored or reused for report continuity. <br>
Mitigation: Use non-sensitive identifiers where possible, avoid phone numbers or guessable identifiers unless separately authenticated, and review local configuration before deployment. <br>
Risk: The generated stroke-risk report is screening guidance and may be incomplete or misleading if treated as diagnosis. <br>
Mitigation: Present outputs as risk-screening information only and direct high-risk or symptomatic users to professional medical evaluation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-stroke-risk-screening-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, api calls, guidance] <br>
**Output Format:** [Markdown or JSON text, depending on the requested detail level] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report export links and historical report lists when returned by the configured service.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter says 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
