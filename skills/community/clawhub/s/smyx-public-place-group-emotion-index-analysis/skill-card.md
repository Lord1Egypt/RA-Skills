## Description: <br>
Analyzes fixed-camera public-place video to produce anonymous group-level emotion distributions, a 0-100 group-emotion index, and operational or safety guidance for venues such as malls and exhibitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External venue operators, safety teams, and developers use this skill to analyze public-place video or report history for aggregate emotion trends, area-level indicators, and human-reviewed operational or safety recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public-place video or video URLs and a stable identifier are sent to the publisher's cloud service. <br>
Mitigation: Use the skill only for deployments with appropriate consent or signage, confirm retention limits, and prefer scoped pseudonymous identifiers over usernames or phone numbers. <br>
Risk: User-linked history/report retrieval and local token storage can expose sensitive operational records if access is too broad. <br>
Mitigation: Limit use to authorized operators, review local credential handling, and avoid storing or sharing identifiers beyond the deployment need. <br>
Risk: Group emotion outputs can be overinterpreted as individual emotional diagnosis or used for automated intervention. <br>
Mitigation: Use aggregate reports only as decision support, keep human review in the loop, and do not make individual decisions or automated interventions from the emotion index. <br>


## Reference(s): <br>
- [Public Place Group Emotion Index API documentation](artifact/references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-public-place-group-emotion-index-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and structured JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a public-place video file or URL and a user-scoped open-id; outputs may include report links, area breakdowns, and heatmap URLs.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
