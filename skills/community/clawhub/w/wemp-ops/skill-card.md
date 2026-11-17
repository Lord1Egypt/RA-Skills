## Description:

Wemp Ops helps an agent run WeChat Official Account operations across topic selection, material collection, article writing, layout formatting, draft publishing, analytics, and comment management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and agent users use this skill to produce WeChat Official Account articles, create cover and inline visual plans, convert Markdown into WeChat-compatible HTML, push drafts, review analytics, and manage reader comments. It is intended for external-facing content operations where account credentials and publishing permissions must be controlled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The evidence reports bundled real-looking WeChat credentials.

Mitigation: Remove bundled credentials before installation, rotate any exposed WeChat secret, and require users to provide account credentials through a controlled secret store or local configuration.

Risk: The evidence reports high-impact account mutation and posting capabilities.

Mitigation: Restrict use to explicit WeChat operations, require human confirmation before publishing, messaging followers, changing account settings, deleting content, or modifying comments, and scope API credentials to the minimum required permissions.

Risk: The evidence calls out unsafe defaults for automatic deletion, retention, and writeback.

Mitigation: Disable automatic cleanup, deletion, retention, and feedback writeback by default, and make each state-changing action opt-in with visible target identifiers.

Risk: The evidence calls out a Markdown upload code-injection bug.

Mitigation: Fix the Markdown upload path before use, sanitize file paths and generated scripts, and avoid executing generated upload code from untrusted Markdown or image paths.

Risk: The evidence says logged-in browser sessions may be used for product screenshots and platform publishing.

Mitigation: Use isolated browser profiles, avoid private pages unless necessary, redact sensitive account or customer data from screenshots, and confirm browser-based publishing actions with the account owner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovensky1992-wk/skills/wemp-ops)
- [README](README.md)
- [Article structure templates](references/article-templates.md)
- [Cover image design guide](references/cover-image-guide.md)
- [Illustration prompt guide](references/illustration-prompts.md)
- [WeChat platform constraints](references/weixin-constraints.md)
- [Writing SOP](references/writing-sop.md)
- [Writing techniques and review method](references/writing-techniques.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown articles, WeChat-compatible HTML, JSON script results, shell commands, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce draft files, image plans, image prompts, local HTML, analytics reports, and proposed or executed WeChat draft, publishing, and comment actions when configured.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
