## Description: <br>
Analyzes plant leaf images or videos to identify curl direction, margin scorch patterns, affected leaf layers, likely causes, confidence, and directional care suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External growers, agronomy teams, and agriculture application developers use this skill to submit plant leaf media for curl and scorch diagnosis and to query previously generated cloud reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant images or videos and report-history queries are sent to remote lifeemergence.com services. <br>
Mitigation: Avoid sensitive farm, facility, worker, or location imagery unless the publisher explains retention, account creation, token storage, and deletion controls. <br>
Risk: The skill can silently create or reuse identities and store local identity or token records in the workspace. <br>
Mitigation: Review the identity and token storage behavior before installation, run in an isolated workspace, and remove local records when they are no longer needed. <br>
Risk: Plant diagnosis may be incomplete or mistaken when visual symptoms overlap across drought, disease, pesticide damage, fertilizer burn, or cold stress. <br>
Mitigation: Treat results as directional guidance, combine them with field inspection and sensor context, and seek professional plant-health advice for severe suspected disease. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-leaf-curling-scorch-diagnosis-analysis) <br>
- [Leaf curl and scorch API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown or JSON diagnostic reports and history lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report export links returned by the remote service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
