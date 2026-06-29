## Description: <br>
Generates condensed album highlights from long videos based on user-specified keywords or target subjects, returning structured analysis results and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit local or URL-based videos and request highlight extraction for people, pets, scenes, or events. It also supports cloud history report retrieval for prior custom time-lapse analyses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Videos, uploaded media, or video URLs may be sent to the publisher's cloud service for processing. <br>
Mitigation: Install only if cloud media processing is acceptable, and use media that is appropriate to send to the publisher's service. <br>
Risk: The skill may silently create or reuse an internal identity and store returned tokens in a local SQLite database. <br>
Mitigation: Review identity and token storage expectations before installation, and prefer a version that explicitly documents token storage and identity handling. <br>
Risk: History-report requests query prior cloud reports associated with the internal identity. <br>
Mitigation: Use history retrieval only in workspaces where that cloud report access is expected, and review returned report links before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-custom-timelapse-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown text with JSON-formatted analysis or history-report records and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local video files or video URLs through the publisher's cloud API and can optionally write the returned report text to a local output file.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter reports 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
