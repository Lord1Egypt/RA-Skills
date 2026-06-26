## Description: <br>
AI-powered pet sneeze/cough detection from real-time camera video with optional audio fusion, producing behavior-level event detection, frequency counts, and history report views for pet respiratory monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External pet owners, animal hospital staff, boarding center staff, and developers can use this skill to analyze pet videos or report history for sneeze and cough behavior patterns. The output is for behavior observation and does not provide a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet videos, household imagery or audio, and persistent open-id values may be sent to remote Life Emergence/SMYX services during analysis or history lookup. <br>
Mitigation: Use the skill only with informed user consent, avoid sensitive footage where possible, and avoid real phone numbers as open-id values unless required and consented to. <br>
Risk: The release includes a bundled API key and account or token persistence behavior noted by the security evidence. <br>
Mitigation: Treat bundled credentials as exposed and review or remove shared account and token persistence paths before deploying in multi-user or sensitive environments. <br>
Risk: Detection results may be mistaken for medical conclusions. <br>
Mitigation: Present results as behavior observations only and direct users to veterinary care for frequent events, breathing difficulty, or other concerning symptoms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-sneeze-cough-detection-analysis) <br>
- [API interface reference](references/api_doc.md) <br>
- [Bundled SMYX analysis API reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-formatted detection reports, Markdown history tables, and optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided or configured open-id before remote analysis or history lookup; accepts local video paths or public video URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
