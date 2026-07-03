## Description: <br>
Analyzes aquarium plant images or videos to identify visual health symptoms, produce structured health assessments, care suggestions, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, aquarium hobbyists, aquascaping shops, and developers use this skill to analyze aquarium plant media for visible color, morphology, algae, and nutrient-deficiency symptoms. It returns a visual health assessment, care direction, and optional history/report links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends aquarium media or media URLs to lifeemergence.com services for analysis. <br>
Mitigation: Use only media you are permitted to share, and avoid private or signed URLs unless you trust the publisher and service. <br>
Risk: The skill creates or reuses local identity state, queries cloud-stored report history, and stores returned tokens in a local SQLite database with limited user control. <br>
Mitigation: Avoid shared workspaces, review local state before reuse, and remove stored credentials or identity state when access should be revoked. <br>
Risk: The security evidence marks the release suspicious because of silent remote authentication and token persistence. <br>
Mitigation: Review the skill and network destinations before deployment, and run it in an isolated environment when evaluating it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-aquarium-plant-health-monitor-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/smyx-sunjinhui) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with structured JSON analysis and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save the analysis result to a local output file when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
