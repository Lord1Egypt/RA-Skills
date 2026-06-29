## Description: <br>
Analyzes pet grooming images, videos, or URLs with server-side APIs to recognize stress behaviors such as struggling, panting, tail tucking, and grooming-stage stress levels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External groomers, veterinary clinics, and pet-care services use this skill to submit grooming-session media for structured stress-behavior analysis, report links, and cloud-backed historical report lookup. The results are intended for behavior observation and workflow triage, not disease diagnosis or treatment planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends grooming images, videos, or media URLs to the LifeEmergence service for analysis. <br>
Mitigation: Use only with appropriate consent for the media being analyzed, and avoid submitting sensitive or unnecessary footage. <br>
Risk: The security scan reports that the skill can create or reuse a persistent account identity, store local account tokens, and retrieve cloud report history. <br>
Mitigation: Review or clear the workspace data directory when account-linked history should not persist, and avoid shared workspaces unless all affected users consent. <br>
Risk: The skill provides behavioral stress observations that could be mistaken for medical or behavior-correction advice. <br>
Mitigation: Treat outputs as advisory observations and have qualified staff or veterinary professionals review severe stress, injury, or health concerns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-pet-grooming-stress-behavior-analysis) <br>
- [Pet grooming stress API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON analysis reports with report links and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include structured stress indicators, report-image export links, and historical report tables retrieved from the cloud API.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
