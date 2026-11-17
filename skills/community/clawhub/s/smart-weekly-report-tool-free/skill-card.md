## Description: <br>
Smart Weekly Report Basic helps an agent turn work logs or conversation context into weekly report drafts, next-week plans, and to-do lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees can use this skill to summarize weekly work activity, draft a structured report, and extract a prioritized to-do list for the next week. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill under-discloses network, API, and callback behavior while claiming free-version data stays local. <br>
Mitigation: Review network egress, callback URL handling, output directories, caching, and API key storage before using the skill with sensitive work content. <br>
Risk: The artifact declares read and exec capabilities and can process local logs or conversation context. <br>
Mitigation: Run it in a scoped workspace with least-privilege file access and review generated report content before sharing or archiving it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/smart-weekly-report-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON-style structured responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report and to-do file paths, status fields, execution logs, and user-confirmation markers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
