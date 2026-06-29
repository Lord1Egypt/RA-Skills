## Description: <br>
Analyzes pet monitoring videos or video URLs for anxiety, howling, and prolonged loneliness signals, then returns structured pet-soothing trigger analysis and report history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and pet-care application developers use this skill to submit pet camera footage for cloud analysis, review structured behavior results, and retrieve historical pet-soothing trigger reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet-camera videos or video URLs may contain sensitive home footage and are sent to the configured cloud analysis service. <br>
Mitigation: Request explicit user confirmation before upload or history lookup, avoid private or internal URLs, and avoid sensitive footage unless retention and deletion terms are clear. <br>
Risk: Report history is tied to an automatically selected local identity and service tokens may be stored in a local SQLite database. <br>
Mitigation: Run only in trusted workspaces, review local data retention, and rotate or remove stored tokens when the skill is no longer needed. <br>
Risk: The release is advertised as an automatic soothing-device trigger, while the artifact behavior mainly returns analysis output and report links. <br>
Mitigation: Treat output as decision support and verify any separate device-control integration before relying on automated pet-soothing actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-pet-calming-trigger-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON text containing analysis results, report links, and report-history listings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are produced from configured cloud analysis APIs; local video inputs are limited to mp4, avi, or mov files up to 10 MB.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release evidence; artifact frontmatter lists 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
