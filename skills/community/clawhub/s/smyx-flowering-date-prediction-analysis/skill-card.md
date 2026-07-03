## Description: <br>
AI-powered flowering-date prediction for ornamental and cut-flower plants that uses flower-bud images or videos, optional temperature and light data, and a pre-trained phenology model to estimate full-bloom dates within the next 3-7 days. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Growers, greenhouse operators, botanical gardens, and flower-tourism teams use this skill to analyze bud-stage media and optional environmental data for flowering-date forecasts, confidence information, phenology-stage reporting, and production-planning guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded media or submitted URLs are sent to a lifeemergence cloud analysis service. <br>
Mitigation: Avoid sensitive images, private URLs, or regulated data unless the deployment has approved that cloud processing path. <br>
Risk: The skill silently creates or reuses a local identity and stores tokens. <br>
Mitigation: Review identity and token storage behavior before installing in shared, locked-down, or privacy-sensitive workspaces. <br>
Risk: Server evidence reports mismatched flower, pet, video, and shared-service behavior. <br>
Mitigation: Review the installed behavior and outputs before relying on predictions for scheduling, harvesting, pollination, or tourism operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-flowering-date-prediction-analysis) <br>
- [Skill API Documentation](artifact/references/api_doc.md) <br>
- [Shared Analysis API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style structured analysis reports with report links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save results to a user-specified output file and may list historical reports as a Markdown table.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
