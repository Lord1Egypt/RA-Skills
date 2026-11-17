## Description:

Guides an agent through publishing long-form or text-only Xiaohongshu posts in the web creator platform, including browser setup, editing, formatting, publishing, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1122525](https://clawhub.ai/user/1122525)

### License/Terms of Use:


## Use Case:

Content creators and social media operators use this skill to publish Xiaohongshu long-form posts more consistently through the web creator workflow. It is intended for agents operating a logged-in browser session with the user's final review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can operate a logged-in Xiaohongshu creator page and submit a real public post for platform review.

Mitigation: Before the final publish action, review the selected account, title, body, tags, location, originality setting, and preview.

Risk: The skill requires browser host control in an active profile.

Mitigation: Enable browser control only for the intended OpenClaw profile and confirm the active logged-in account before running the publishing steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1122525/skills/rednote-publisher)
- [Xiaohongshu creator publishing page](https://creator.xiaohongshu.com/publish/publish?source=official)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline JSON configuration and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes browser-control steps and checkpoints for reviewing content before publication.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
