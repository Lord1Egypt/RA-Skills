## Description: <br>
Analyzes uploaded or URL-based pet media through cloud APIs to produce structured pet health reports with condition signals, care suggestions, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and pet-care assistants use this skill to submit cat, dog, bird, or other pet videos or image files for cloud health analysis and to retrieve prior Pet Safety Guardian reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet videos or URLs are sent to the Life Emergence backend for analysis. <br>
Mitigation: Use the skill only with media and URLs that are acceptable to share with that backend; avoid private home footage or sensitive URLs unless authorization and retention terms are clear. <br>
Risk: The skill silently creates or reuses an internal identity and stores auth tokens in a local workspace database. <br>
Mitigation: Deploy only where this identity and token behavior is acceptable, and review account-control and local storage handling before use. <br>
Risk: Cloud report history can be fetched automatically when prompted with under-scoped identity controls. <br>
Mitigation: Limit use to contexts where the publisher's report-history authorization behavior is understood and acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Files, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, JSON responses, report links, and optional output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include structured health findings, care suggestions, historical report tables, and links to exported reports.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
