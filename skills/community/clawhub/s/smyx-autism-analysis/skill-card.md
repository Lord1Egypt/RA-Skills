## Description: <br>
Analyzes child behavior videos for Autism Spectrum Disorder characteristics and returns structured findings, risk indicators, report links, and intervention suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as parents, educators, and care professionals can use this skill to submit a child behavior video or public video URL for preliminary ASD-related behavior analysis. The skill can also retrieve cloud-stored historical analysis reports for the automatically associated account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud processing may involve real children's videos or health-related information. <br>
Mitigation: Use only media you are authorized to process and avoid highly sensitive media unless the publisher provides acceptable privacy, retention, and deletion terms. <br>
Risk: The skill automatically creates or reuses an account-linked identity and stores tokens locally. <br>
Mitigation: Run it in a controlled workspace, review local token and database storage before deployment, and clear stored credentials when they are no longer needed. <br>
Risk: Historical report retrieval can expose sensitive prior analysis reports. <br>
Mitigation: Confirm the account context before listing reports and avoid sharing report links outside the authorized audience. <br>
Risk: ASD analysis output may be mistaken for a clinical diagnosis. <br>
Mitigation: Treat results as preliminary screening support only and defer diagnosis or treatment decisions to qualified medical professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-autism-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown text with embedded structured JSON and optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report export links and cloud historical report lists; supports basic, standard, and JSON detail levels.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
