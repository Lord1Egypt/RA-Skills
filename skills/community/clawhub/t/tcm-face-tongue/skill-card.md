## Description: <br>
Calls RageHealth face and tongue TCM APIs to analyze uploaded face or tongue photos and return constitution, organ yin-yang scores, symptoms, face or tongue classifications, recipes, and combined interpretations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianchen94](https://clawhub.ai/user/qianchen94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run TCM-style face, tongue, or combined face-tongue analysis from user-provided images and produce an informational report with constitution, symptom, organ balance, tongue or face feature, and dietary guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sensitive face or tongue photos and optional age, gender, skin, IP, or location data to RageHealth for processing. <br>
Mitigation: Use the skill only with consent from the person in the images, send only the optional fields needed for the request, and keep TCM_AK and TCM_SK credentials private. <br>
Risk: Outputs are health-adjacent TCM interpretations and may be mistaken for medical diagnosis. <br>
Mitigation: Present results as informational only, avoid definitive medical claims, and recommend licensed clinical care for severe, persistent, or concerning symptoms. <br>
Risk: Enabling faceIdDetect can involve face feature data linked to a user group. <br>
Mitigation: Enable faceIdDetect only when specifically needed and explicitly authorized, and avoid creating persistent face identifiers by default. <br>
Risk: Combined analysis with local image files falls back to separate face and tongue calls and does not include the service-generated comprehensive interpretation. <br>
Mitigation: Disclose when fallback output is used and avoid overstating any combined conclusion when comprehensiveInterpretation is missing. <br>


## Reference(s): <br>
- [Tcm Face Tongue on ClawHub](https://clawhub.ai/qianchen94/tcm-face-tongue) <br>
- [Response schema](references/response_schema.md) <br>
- [RageHealth credential portal](https://chayan-test.ragehealth.cn/client) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write full API responses to JSON files; default terminal output omits large landmark and polygon arrays unless full output is requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
