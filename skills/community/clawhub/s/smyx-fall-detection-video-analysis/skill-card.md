## Description: <br>
Detects fall events in target areas from video streams for home safety monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze local video files or video URLs for fall-detection scenarios, retrieve structured reports, and review cloud-hosted historical analysis results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Home-safety videos or video URLs may be processed by configured lifeemergence.com cloud services. <br>
Mitigation: Test first with non-sensitive footage and confirm privacy, retention, and account-deletion terms with the publisher before using sensitive video. <br>
Risk: Cloud report history is tied to an automatically selected identity. <br>
Mitigation: Avoid exposing identity values to users and verify how report association, retention, and deletion are handled before deployment. <br>
Risk: The skill stores user or token data locally in the workspace. <br>
Mitigation: Run in an isolated workspace, restrict access to local state, and clear stored credentials or user data when the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-fall-detection-video-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [Fall detection video API documentation](artifact/references/api_doc.md) <br>
- [Common analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON analysis reports with report links and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured detection results, risk prompts, recommendations, saved output files, and historical report tables.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter lists 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
