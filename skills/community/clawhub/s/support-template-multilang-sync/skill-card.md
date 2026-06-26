## Description: <br>
Update multilingual customer support reply templates in markdown files, then sync the updated content to Feishu Wiki, log the change in a GitHub issue, and package/publish the repeatable workflow to ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support operations teams and developers use this skill to update multilingual support-template markdown, preserve placeholder consistency, mirror approved content to Feishu Wiki, and record the change in GitHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can update support-template files and publish or sync content to external systems. <br>
Mitigation: Require a dry run and explicit human approval before each Feishu sync, GitHub issue, SKILL.md update, or ClawHub publish action. <br>
Risk: Feishu, GitHub, and ClawHub credentials may be needed for the workflow. <br>
Mitigation: Store credentials in environment variables or a secret store, use least-privilege tokens, and do not paste secrets into prompts or generated content. <br>
Risk: Template edits can accidentally change placeholders, language coverage, or support tone. <br>
Mitigation: Re-read the final markdown and verify placeholders, language sections, bullet alignment, and headings before syncing or logging the update. <br>


## Reference(s): <br>
- [Publishing Notes](references/publishing-notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/support-template-multilang-sync) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text guidance with optional generated issue-body text and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Feishu, GitHub, and ClawHub credentials for external sync and publishing steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
