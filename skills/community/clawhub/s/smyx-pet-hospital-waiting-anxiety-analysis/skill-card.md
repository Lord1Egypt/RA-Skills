## Description: <br>
Analyzes pet hospital waiting-area video or video URLs through remote APIs to estimate a 1-5 pet anxiety level from observable stress signals such as panting, trembling, ear posture, hiding, stiffness, licking, and yawning, without diagnosing disease or prescribing treatment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External veterinary staff, clinic operators, and agent users can use this skill to triage waiting-area pets by generating an anxiety-level report from video evidence. The report is intended as workflow support and should be reviewed alongside professional veterinary judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet hospital video footage and user identifiers are sent to publisher-operated remote services. <br>
Mitigation: Use only with footage and identifiers approved for that service, and confirm data handling, retention, and access controls before using real clinic footage. <br>
Risk: The security review flags under-disclosed account, token, history, and backend-management behavior. <br>
Mitigation: Review the skill's account and token flow before installation, require explicit user-controlled credentials, and limit deployment to environments where that behavior is acceptable. <br>
Risk: The output estimates anxiety from video and may be affected by footage quality, species, breed, and context. <br>
Mitigation: Treat results as triage support only and require veterinary staff to make final care and prioritization decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-pet-hospital-waiting-anxiety-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Common analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with structured JSON-style analysis results and optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include anxiety level, observed behavior signals, report-list output, and report export links returned by the remote service.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
