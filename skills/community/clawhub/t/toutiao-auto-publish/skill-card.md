## Description:

Automates posting short text, topics, and optional images to Toutiao Weitoutiao through a browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devilsbibble](https://clawhub.ai/user/devilsbibble)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and developers use this skill to prepare and run Toutiao Weitoutiao publishing automation for short posts with optional topics and images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automation can publish using the active logged-in Toutiao browser session without a final confirmation step.

Mitigation: Require an explicit review and confirmation before publishing, and run the automation from an isolated browser profile.

Risk: The script may change the supplied post text by appending default filler or topics before publishing.

Mitigation: Review the exact final text before publishing and modify the script to publish only user-approved content.

Risk: Browser automation injects post content into the page and depends on local Playwright and browser behavior.

Mitigation: Pin dependencies, review the script before installation, and avoid interpolating untrusted content into JavaScript.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devilsbibble/skills/toutiao-auto-publish)
- [Toutiao creator portal](https://mp.toutiao.com)
- [Toutiao Weitoutiao publishing URL](https://mp.toutiao.com/profile_v4/weitoutiao/publish?from=toutiao_pc)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create success or error screenshots on the user's Desktop when the automation is run.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
