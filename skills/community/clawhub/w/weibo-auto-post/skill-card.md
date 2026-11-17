## Description:

Generates Weibo post images with PIL, prepares content strategy guidance, and automates browser-based Weibo publishing through clipboard paste and desktop controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apple-sugar-xing](https://clawhub.ai/user/apple-sugar-xing)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and operators use this skill to generate Weibo-ready image cards, plan recurring content formats, and automate posting from a logged-in browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish publicly through a logged-in Weibo browser session without a final confirmation step.

Mitigation: Require manual review and confirmation immediately before clicking publish.

Risk: Scheduled posting can run unattended and publish stale, duplicate, or inappropriate content.

Mitigation: Disable cron jobs by default and require approval for each scheduled payload before enabling it.

Risk: Temporary-file cleanup can delete matching local files.

Mitigation: Use a dedicated output directory and review cleanup patterns before running the publish workflow.

Risk: Desktop automation controls the active browser session and clipboard.

Mitigation: Run it in an isolated browser profile or controlled desktop session that is logged in only to the intended Weibo account.

Risk: PowerShell image-path handling can treat path content as command text.

Mitigation: Pass image paths as data through safe argument binding before using the publishing script.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apple-sugar-xing/skills/weibo-auto-post)
- [Weibo Content Types Guide](references/content_types.md)
- [Weibo Cron Guide](references/cron_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger browser automation, clipboard writes, public posting, scheduled runs, and local temporary-file cleanup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
