## Description: <br>
Manages post-posting bookkeeping for approved Reddit drafts after a human confirms the live Reddit URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lknezic](https://clawhub.ai/user/lknezic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Operators who coordinate Reddit posting use this skill after Luka manually posts an approved draft, so the agent can archive the posted draft, attach the Reddit URL, update active task records, and log outcome signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The support material includes account-warming, karma-building, and anti-detection guidance that could be used to bypass subreddit or platform rules. <br>
Mitigation: Review or remove that guidance before installation, and limit use to local bookkeeping after a human-confirmed post. <br>
Risk: The workflow modifies local posting records and deletes the pending draft after archiving. <br>
Mitigation: Verify the APPROVED decision file, confirm the live Reddit URL, and confirm the posted copy exists before deleting the pending draft. <br>


## Reference(s): <br>
- [Reddit Post Skill](artifact/SKILL.md) <br>
- [Posting Settings Reference](artifact/ref-settings.md) <br>
- [Safety and Anti-Detection Rules](artifact/ref-safety.md) <br>
- [ClawHub skill page](https://clawhub.ai/lknezic/reddit-post) <br>
- [Publisher profile](https://clawhub.ai/user/lknezic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown file updates and concise status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local bookkeeping updates only; it does not submit content to Reddit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
