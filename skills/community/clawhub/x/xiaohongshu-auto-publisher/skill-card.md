## Description:

Posts content (images/videos) to Xiaohongshu (Little Red Book) automatically using Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[widebluesky](https://clawhub.ai/user/widebluesky)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to automate Xiaohongshu publishing of supplied titles, captions, and image or video files after establishing a browser login session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable Xiaohongshu login session is stored in state.json.

Mitigation: Treat state.json as a sensitive login token: do not share, sync, archive, or commit it, and delete or rotate the session when finished.

Risk: The automation can publish supplied title, text, and files without a final confirmation step.

Mitigation: Review the generated post in the visible browser before relying on the automation, and keep manual intervention available for popups or captchas.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/widebluesky/skills/xiaohongshu-auto-publisher)
- [Xiaohongshu Creator login](https://creator.xiaohongshu.com/login)
- [Xiaohongshu Creator publish page](https://creator.xiaohongshu.com/publish/publish)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with command-line examples and browser automation status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a saved browser session and may open a visible browser for login, popups, captchas, upload review, and publishing.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
