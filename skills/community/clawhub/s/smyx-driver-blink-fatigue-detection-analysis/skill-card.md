## Description: <br>
Analyzes driver face video or image inputs to estimate eye state, blink rate, eye-closure duration, PERCLOS, fatigue level, warnings, recommendations, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and fleet safety teams use this skill to submit driver monitoring video or image inputs for fatigue-oriented eye-state analysis and to retrieve structured historical reports. The output is an auxiliary safety signal, not a medical diagnosis or a substitute for driver judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Driver video may contain biometric or workplace monitoring data and is sent to LifeEmergence cloud services for analysis. <br>
Mitigation: Use only with informed driver consent, a lawful basis for processing, and documented retention, deletion, and access-control expectations. <br>
Risk: The skill can create or reuse local identity state and store authentication tokens locally. <br>
Mitigation: Run it only in trusted workspaces, restrict local file access, rotate credentials when needed, and review whether token storage is acceptable for the device. <br>
Risk: Fatigue warnings can be affected by poor video quality, sunglasses, glare, occlusion, low frame rate, or missing eye visibility. <br>
Mitigation: Treat outputs as auxiliary safety signals, verify camera placement and input quality, and require human operational judgment for safety-critical decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-driver-blink-fatigue-detection-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown text with structured JSON analysis content and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include fatigue metrics, warning categories, recommended actions, historical report lists, and exported report URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
