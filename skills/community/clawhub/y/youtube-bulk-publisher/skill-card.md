## Description:

Uploads videos to YouTube with configurable titles, descriptions, tags, categories, privacy settings, optional thumbnails, progress reporting, and status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly3094](https://clawhub.ai/user/fly3094)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, operators, and developers use this skill to automate YouTube video publishing through a command-line tool or Python interface. It supports OAuth setup, upload metadata, privacy selection, optional thumbnail upload, and uploaded-video status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth token storage is unsafe because the skill stores and loads account tokens from a pickle file in the skill credentials directory.

Mitigation: Review before installing, run only from a trusted private directory, use a test or intended YouTube account, and replace token storage with a non-executable private-permission format before broader use.

Risk: The skill can publish videos with user-provided metadata and privacy settings to a YouTube account.

Mitigation: Verify every video, thumbnail, title, description, tag list, category, and privacy setting before upload; use private or unlisted visibility until publication details are confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fly3094/skills/youtube-bulk-publisher)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown guidance with command-line examples, Python snippets, console progress text, and structured upload result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate YouTube Data API uploads and OAuth authorization when executed by an agent in a configured environment.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
