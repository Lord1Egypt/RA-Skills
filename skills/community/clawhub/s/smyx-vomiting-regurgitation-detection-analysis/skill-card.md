## Description: <br>
Detects pet vomiting and regurgitation behavior from indoor fixed-camera video and reports visual event timing, frequency, action features, and vomitus characteristics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, pet owners, pet-care teams, and animal hospital staff use this skill to analyze indoor pet videos or video URLs for visual signs of vomiting or regurgitation. The output is intended for behavior observation and report review, not veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indoor pet videos or video URLs may contain private household information and are sent to an external LifeEmergence/SMYX cloud service for analysis. <br>
Mitigation: Use only non-sensitive footage, confirm consent for uploaded media, and avoid sending videos from private or regulated environments unless the publisher's retention and deletion terms are acceptable. <br>
Risk: The skill can silently create or reuse an account identity and associate analysis reports with that identity. <br>
Mitigation: Run the skill in a dedicated workspace and review publisher documentation for account creation, authorization, report access, and deletion controls before operational use. <br>
Risk: Access tokens and identity data may be stored locally and reused for future requests. <br>
Mitigation: Avoid shared workspaces, protect the workspace data directory, rotate or remove local credentials after use, and reinstall only when local token storage is acceptable. <br>
Risk: Cloud report history can be retrieved by the skill, which may expose prior analysis records and report links. <br>
Mitigation: Limit use to trusted users and environments, and confirm that historical report visibility matches the intended privacy boundary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-vomiting-regurgitation-detection-analysis) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-like structured text, with optional saved text output files and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload local video files or submit video URLs to the LifeEmergence/SMYX cloud service; history listing returns structured report records and report links.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub server release evidence; artifact frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
