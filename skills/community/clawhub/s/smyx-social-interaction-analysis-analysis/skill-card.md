## Description: <br>
Analyzes multi-pet images or videos to classify social interactions, quantify duration, frequency, initiators, and receivers, and return structured social-behavior reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, pet-care operators, and behavior-clinic staff use this skill to submit multi-pet footage or a video URL and receive structured observations about interaction types, participants, frequency, duration, conflict signals, and report links. The skill is for behavior observation support and does not provide medical or training advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet videos or video URLs may be processed by the publisher's cloud service. <br>
Mitigation: Use only when the publisher's privacy, retention, and deletion terms are acceptable; avoid sensitive household footage. <br>
Risk: Report history may be tied to an automatically managed persistent identity with local storage of user records and tokens. <br>
Mitigation: Use a separate workspace for evaluation and clear local state and tokens according to organizational policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-social-interaction-analysis-analysis) <br>
- [API 接口文档](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands] <br>
**Output Format:** [Markdown report text with optional JSON details and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the generated report to a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
