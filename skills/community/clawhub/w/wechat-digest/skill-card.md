## Description: <br>
Extract, summarize, and synthesize WeChat public account articles into structured knowledge cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and readers use this skill to turn public WeChat articles into concise summaries, structured knowledge cards, Markdown notes, or cross-article synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands in maintainer workflows could affect the wrong repository, account, or deployment. <br>
Mitigation: Confirm the target before running moderation, migration, email, or autoreview commands and use documented dry-run, backup, confirmation, and opt-out controls. <br>
Risk: Article summaries and extracted quotes may over-retain source material or misrepresent the source article. <br>
Mitigation: Use the skill for summaries and extracts rather than full-text republication, review generated notes before sharing, and skip paywalled content. <br>


## Reference(s): <br>
- [Output Formats Reference](references/formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown, plain text, and JSON knowledge-card structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print structured notes to stdout or write batch outputs to files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
