## Description:

Drafts a Reddit post for a specific subreddit that follows its rules, then gives the user a prefilled reddit.com link to review and post it themselves. Never posts automatically. Use when the user wants to share something on Reddit or a subreddit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

External users who want to share something on Reddit can use this skill to prepare one post draft that follows a chosen subreddit's rules, review the prefilled submission, and post it themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening the prefilled submission link sends the draft content to Reddit.

Mitigation: Review the subreddit, title, text or link, and flair before opening the submission link.

Risk: Initialization depends on socialkit-social-core, which is outside this assessment.

Mitigation: Review the separate dependency before running its initialization command.

## Reference(s):

- [Reddit setup guide](artifact/references/setup.md)

## Skill Output:

**Output Type(s):** [Text, Configuration, Shell commands]

**Output Format:** [A Reddit post draft and prefilled submission URL, with draft data in JSON and user guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One subreddit per draft; includes a title and text or link, with optional flair. Posting remains under the user's control.]

## Skill Version(s):

0.3.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
