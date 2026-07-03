## Description: <br>
Analyzes consented nighttime home video for lights-off timing and early-morning activity, compares results with a personal baseline, and reports sleep-rhythm anomaly indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Families, community care workers, and remote-care operators use this skill to analyze nighttime camera video for living-alone sleep rhythm changes and review generated anomaly reports. The output is intended to support follow-up and care checks, not to provide a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send highly sensitive home night video and identifiers to remote services. <br>
Mitigation: Use it only with clear consent, trust in the service provider, and appropriate retention, encryption, and access-control practices. <br>
Risk: Automatic identity handling and historical report retrieval can expose personal monitoring history if account access is not controlled. <br>
Mitigation: Review account security, restrict who can request history, and avoid exposing internal identity values in user-facing output. <br>
Risk: Sleep-rhythm anomaly indicators may be mistaken for medical diagnosis or emergency guidance. <br>
Mitigation: Treat results as visual rhythm observations and confirm anomalies through family, community, or clinical follow-up before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-living-alone-rhythm-anomaly-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and JSON report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include anomaly classifications, care-check guidance, report links, and saved output files when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
