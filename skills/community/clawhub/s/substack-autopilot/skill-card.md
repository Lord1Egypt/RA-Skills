## Description: <br>
Automate drafting and local saving of weekly Substack articles from a topic queue, opening the editor for final human review before publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoqi](https://clawhub.ai/user/caoqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, newsletter operators, and content teams use this skill to turn a managed topic queue into weekly Substack draft Markdown, update local tracking files, open Substack for review, and send Telegram status notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill edits local workflow files for the topic queue, article log, and generated drafts. <br>
Mitigation: Configure a narrow workspace folder and keep backups or version control for article-topics.json and article-log.json. <br>
Risk: Generated article drafts may contain incorrect claims, weak brand fit, or inappropriate calls to action. <br>
Mitigation: Preserve the documented quality check and human review step before publishing in Substack. <br>
Risk: Browser and Telegram actions can target the wrong publication or recipient if placeholders are misconfigured. <br>
Mitigation: Verify the Substack publication URL and Telegram recipient before enabling the cron workflow. <br>


## Reference(s): <br>
- [Article Angle Frameworks](references/article-angles.md) <br>
- [Cron Job Prompt Template](references/cron-prompt-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown drafts, JSON file updates, browser review instructions, and Telegram notification text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates article-topics.json, article-log.json, and article-YYYY-MM-DD.md; leaves publishing to human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
