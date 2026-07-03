## Description: <br>
Analyzes pet water fountain area videos or video URLs through a cloud service to produce structured drinking-frequency, duration, estimated-intake, baseline-comparison, and anomaly-warning reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze pet water-fountain camera footage, review drinking behavior metrics, and query cloud-hosted historical reports. The output is for health monitoring and early warning context, not medical diagnosis or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet or household video may be uploaded to the Life Emergence cloud service for analysis. <br>
Mitigation: Use only footage you are authorized to process, avoid sensitive household scenes, and confirm service retention, deletion, and access-control terms before deployment. <br>
Risk: The skill can create or reuse an internal identity and store tokens or history state in the workspace data directory. <br>
Mitigation: Run in an isolated workspace, protect local data files, review account-control behavior, and delete local state when the skill is no longer needed. <br>
Risk: Drinking-intake estimates and health warnings may be mistaken for diagnosis. <br>
Mitigation: Treat outputs as monitoring signals only and route medical decisions to a qualified veterinarian. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-water-fountain-intake-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Analysis API Interface Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-like structured text with report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write output to a user-specified file and may query cloud-hosted report history.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
