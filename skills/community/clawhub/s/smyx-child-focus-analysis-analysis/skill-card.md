## Description: <br>
Analyzes camera footage of a child's study area to estimate per-minute focus scores, identify distraction events, generate structured reports, and retrieve cloud-stored report history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze child study-area video files or URLs for focus scores, distraction periods, structured reports, and historical report retrieval. Parents and teachers can use the results as auxiliary study-behavior indicators, not as a substitute for direct supervision or educational judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends children's study videos or video URLs to a Life Emergence cloud service. <br>
Mitigation: Use only with appropriate guardian consent and review retention, deletion, export, and access policies before processing minors' video. <br>
Risk: Reports are linked to a silently managed persistent local identity. <br>
Mitigation: Verify identity linkage, access control, and who can retrieve historical reports before deployment. <br>
Risk: Focus scores and distraction labels can be overinterpreted as definitive educational or behavioral judgments. <br>
Mitigation: Present results as auxiliary visual indicators and require parent or teacher review for decisions. <br>


## Reference(s): <br>
- [Child Focus Analysis API Documentation](references/api_doc.md) <br>
- [Shared Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files] <br>
**Output Format:** [Markdown text with structured JSON report content and optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud report export links and historical report lists.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
