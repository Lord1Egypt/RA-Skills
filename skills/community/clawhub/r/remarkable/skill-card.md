## Description:

Send files and web articles to a reMarkable e-ink tablet via the reMarkable Cloud, including PDF and EPUB upload, article conversion, and cloud file browsing or management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickian](https://clawhub.ai/user/nickian)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to send documents or readable web-article ebooks to a reMarkable tablet and to list, search, create folders, and upload files through the reMarkable Cloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent reMarkable Cloud credentials are cached locally at ~/.rmapi.

Mitigation: Treat ~/.rmapi as sensitive account access and restrict local account, filesystem, and backup exposure.

Risk: The skill fetches arbitrary web URLs and uploads local documents or converted articles to reMarkable Cloud.

Mitigation: Avoid private URLs or documents unless the user is comfortable with local fetching and cloud upload.

Risk: The setup path builds rmapi from an unpinned source and installs it as a system-wide helper.

Mitigation: Use a trusted, pinned rmapi build and avoid running the skill or installer with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickian/skills/remarkable)
- [rmapi](https://github.com/ddvk/rmapi)
- [reMarkable browser device code](https://my.remarkable.com/device/browser?showOtp=true)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and generated EPUB, PDF, or HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses rmapi for cloud operations and can fetch web URLs locally before upload.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
