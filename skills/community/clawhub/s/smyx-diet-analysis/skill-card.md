## Description: <br>
Analyzes dining videos or video URLs to assess eating behavior, dietary habits, and dietary patterns, then returns structured reports and nutrition improvement guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit dining videos or public video URLs for diet-behavior analysis, including eating speed, habits, food structure, risk signals, and improvement suggestions. The skill can also retrieve prior analysis reports for a provided user identifier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dining videos or video URLs, user identifiers, and analysis history may be sent to Lifeemergence/SMYX cloud services. <br>
Mitigation: Use only after publisher review and user acceptance; require explicit consent before uploads or history retrieval. <br>
Risk: Cloud account, token storage, local SQLite retention, history access, and delete or CRUD behavior are under-documented. <br>
Mitigation: Ask the publisher to document and minimize these behaviors before deployment. <br>
Risk: The output is health-adjacent diet guidance and may be mistaken for professional nutrition or medical advice. <br>
Mitigation: Present results as informational support only and direct users to qualified professionals for diagnosis or treatment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-diet-analysis) <br>
- [API reference](references/api_doc.md) <br>
- [SMYX analysis API reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown or JSON analysis report with optional report export links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include health-adjacent observations, nutrition suggestions, risk warnings, and historical report listings.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
