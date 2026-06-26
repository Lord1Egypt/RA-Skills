## Description: <br>
Analyzes indoor pet-camera videos or video URLs through a remote API to identify pet mouth contact with hazardous non-food items such as wires or plastic and return pica-behavior warnings without providing medical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze indoor pet-monitoring videos for possible pica behavior involving hazardous non-food objects and to receive structured warnings, report links, and intervention guidance. It can also retrieve prior cloud reports associated with the skill's internally managed identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indoor pet-camera footage and identity-linked metadata are sent to a configured remote service for analysis. <br>
Mitigation: Use only with videos and environments approved for remote processing, and avoid footage containing sensitive household or personal information unless that transfer is acceptable. <br>
Risk: The skill can silently create or reuse a local identity and store service tokens in a workspace SQLite database. <br>
Mitigation: Install only in workspaces with acceptable identity isolation, restrict shared workspace access, and clean up local identity and token storage when the skill is no longer needed. <br>
Risk: History queries can enumerate prior cloud reports associated with the managed identity. <br>
Mitigation: Limit use of history retrieval to users authorized to view those reports and review outputs for unintended disclosure before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-pet-pica-behavior-recognition-analysis) <br>
- [Pet pica behavior API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown or structured JSON text with warning details, risk level, report links, and optional history tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the same text output to a user-specified file and may include report export URLs returned by the remote service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
