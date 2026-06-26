## Description: <br>
Detects people, vehicles, non-motorized vehicles, pets, and related activity in outdoor monitoring media, with support for batch image analysis and structured reports for courtyards, orchards, farms, and similar areas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to analyze outdoor surveillance images or videos for intrusions, object counts, risk levels, and report links. It can also query cloud-stored historical monitoring reports for the current internally resolved identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Surveillance images or videos are sent to the provider's cloud service for analysis. <br>
Mitigation: Use only with media that is appropriate for the provider's cloud processing terms, and review account, retention, and deletion expectations before processing sensitive property or personal footage. <br>
Risk: The skill silently creates or reuses remote identity state and may read a workspace identity file. <br>
Mitigation: Review identity handling before deployment and avoid running the skill in workspaces where unintended identity files or account state could be reused. <br>
Risk: Returned session tokens may be stored in a local SQLite database. <br>
Mitigation: Restrict filesystem access to the skill workspace, protect local database files, and remove stored tokens when the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-outdoor-monitoring-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [Outdoor monitoring API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-like structured analysis text with report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the analysis output to a local file when the optional output path is supplied.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
