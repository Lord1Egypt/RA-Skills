## Description: <br>
Use smart journal monitor for evidence insight workflows that need structured execution, explicit assumptions, and clear output boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to rank supplied journal article records by simple breakthrough heuristics, then return a bounded digest with scores, article titles, journals, assumptions, and limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expect live RSS polling, AI summarization, scheduled alerts, or journal fetching because the skill name and documentation overstate those capabilities. <br>
Mitigation: Present this release as a local article-record scoring helper and require supplied JSON article files. <br>
Risk: The script reads article data from a user-provided JSON path. <br>
Mitigation: Provide only article files that are appropriate to read in the workspace and review generated output before using it as a research digest. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/smart-journal-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with plain-text command output from the local Python helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranks JSON article records locally; this release does not provide live RSS polling, AI summarization, scheduled alerts, or journal fetching.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
