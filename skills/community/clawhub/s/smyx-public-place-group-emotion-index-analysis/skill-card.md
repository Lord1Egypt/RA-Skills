## Description: <br>
Analyzes public-place image or video inputs with a remote service to produce anonymous group-level emotion distribution, a 0-100 group emotion index, region breakdowns, operational recommendations, safety guidance, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External venue operators and developers use this skill to analyze fixed-camera public-place media from malls, exhibitions, scenic areas, museums, airports, and similar spaces. It supports customer-satisfaction monitoring, service-layout optimization, and human-reviewed public-safety triage based on aggregate emotion metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public-place media is sent to the publisher's remote service for analysis. <br>
Mitigation: Use only authorized footage, confirm visible notice and consent requirements for the deployment location, and review the publisher's retention and access-control terms before use. <br>
Risk: The skill maintains local account or session state for report history. <br>
Mitigation: Review how identity values and tokens are created, stored, transmitted, rotated, and deleted before installing in a shared or production environment. <br>
Risk: Emotion-analysis outputs could be over-relied on for public-safety or customer-treatment decisions. <br>
Mitigation: Treat results as aggregate operational signals requiring human review, and do not use them for individual identification, differential pricing, or automated intervention. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-public-place-group-emotion-index-analysis) <br>
- [Third-party publisher profile](https://clawhub.ai/user/18072937735) <br>
- [API documentation](references/api_doc.md) <br>
- [Skill usage demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style structured text with report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write results to a user-specified file and may include cloud-hosted report export links.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
