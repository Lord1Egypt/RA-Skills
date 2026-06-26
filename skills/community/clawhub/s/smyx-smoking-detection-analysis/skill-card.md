## Description: <br>
Detects smoking behavior in public-area images, videos, and video streams, then returns structured analysis with violation alerts, recommendations, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Facility, community, and enterprise safety teams can use this skill to analyze media or media URLs for smoking-control monitoring, violation alerts, and cloud report lookup. Developers and agents can invoke the bundled commands to produce structured reports or history tables for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media or media URLs may be sent to external lifeemergence/open API services. <br>
Mitigation: Use only media approved for external processing, and confirm authorization, retention, and deletion controls before using sensitive content. <br>
Risk: The skill can create or reuse a local identity and store authentication tokens in a workspace SQLite database. <br>
Mitigation: Run it in an isolated workspace, restrict access to generated local data, and rotate or remove stored tokens when they are no longer needed. <br>
Risk: Cloud history retrieval has weak visible scoping in the available evidence. <br>
Mitigation: Confirm report access controls with the publisher and review retrieved reports before sharing or acting on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-smoking-detection-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Documentation](references/api_doc.md) <br>
- [Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown text with structured JSON analysis, report links, and optional Markdown tables for cloud history.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save JSON results to a file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact frontmatter lists 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
