## Description: <br>
Detects people, vehicles, non-motorized vehicles, pets, and parcels in video streams or images for general security surveillance scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and security operations developers use this skill to submit surveillance images, videos, or media URLs for object detection, structured reports, and report-history retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Surveillance images, videos, media URLs, identity metadata, and report history may be sent to the publisher's remote services. <br>
Mitigation: Install only after approving remote processing for this data category and confirming retention, deletion, and access expectations with the publisher. <br>
Risk: The skill can quietly create or reuse a persistent identity and store account tokens in a local SQLite database. <br>
Mitigation: Run in an isolated workspace or approved agent environment, review local token storage, and clear stored credentials when the skill is no longer needed. <br>
Risk: Historical report retrieval automatically queries the cloud service when matching user intent is detected. <br>
Mitigation: Limit use to contexts where automatic report-history queries are acceptable and ensure users understand that report retrieval depends on remote account state. <br>


## Reference(s): <br>
- [API interface documentation](references/api_doc.md) <br>
- [Common analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-basic-object-detection-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown and JSON text, with optional saved result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include object counts, confidence-filtered detection results, risk or recognition notes, report links, and report-history tables.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence; artifact frontmatter lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
