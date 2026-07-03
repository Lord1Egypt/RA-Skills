## Description: <br>
Analyzes facial micro-expressions in images or videos through a vendor cloud API and returns structured emotional-state reports, historical report data, suggestions, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit face images or videos for micro-expression and emotion analysis, then receive structured reports and account-linked history from the vendor service. It is most appropriate for low-stakes review, user-facing summaries, and exploratory behavioral analysis rather than decisions that affect rights, access, employment, care, or safety. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face images or videos are sent to the publisher's cloud service for emotion analysis. <br>
Mitigation: Use only media the user is authorized to process, avoid sensitive or high-stakes scenarios, and disclose that analysis is remote before execution. <br>
Risk: The skill silently creates or reuses a persistent local and remote identity and persists account tokens. <br>
Mitigation: Run in an isolated workspace when possible, review or remove local token storage after use, and avoid sharing workspaces across unrelated users. <br>
Risk: Historical report lookup accesses account-linked sensitive analysis data. <br>
Mitigation: Treat report lists and export links as sensitive, return only the records needed for the current user request, and avoid exposing identity values or tokens. <br>
Risk: Micro-expression and emotion outputs can be misleading, especially with poor video quality, face occlusion, lighting issues, or high-stakes interpretation. <br>
Mitigation: Present results as informational, preserve the skill's limitations in user-facing summaries, and require human review before relying on outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-emotion-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Structured text, Markdown tables or JSON depending on the detail mode, with report export links when returned by the service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally write the analysis output to a local file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.9 (source: evidence.json release.version; artifact frontmatter reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
