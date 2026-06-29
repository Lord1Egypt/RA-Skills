## Description: <br>
Detects pet sneeze and cough events from video, with optional audio fusion, and returns structured behavior reports with event timing, frequency, risk prompts, recommendations, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and pet-care operators use this skill to analyze pet activity videos for sneeze and cough behavior, distinguish occasional events from repeated bursts, and review structured reports or cloud report history. The output is behavior observation support only and is not a veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet video or audio and identifiers are processed by LifeEmergence cloud services. <br>
Mitigation: Use only media that is appropriate for external cloud processing, and obtain any required user or organizational approval before running analysis or history queries. <br>
Risk: The skill silently creates or reuses an internal identity and queries cloud report history. <br>
Mitigation: Review local identity behavior and cloud-history access before deployment, especially in shared workspaces or environments with multiple users. <br>
Risk: Authentication tokens and profile data may be stored in a local workspace database. <br>
Mitigation: Run the skill in a controlled workspace, restrict filesystem access, and clear local token/profile storage when the skill is no longer needed. <br>
Risk: Behavior detection output may be mistaken for medical diagnosis. <br>
Mitigation: Present results as observation support only and route frequent, severe, or uncertain respiratory events to a veterinarian. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-sneeze-cough-detection-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [API documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown text with embedded structured JSON and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save analysis output to a file; history queries return a structured report list from the cloud service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
