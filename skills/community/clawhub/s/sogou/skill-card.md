## Description:

Helps agents organize public Sogou Input Method information about features, platform downloads, support resources, privacy, and permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find and summarize official public information about Sogou Input Method features, platform-specific downloads, help resources, privacy, permissions, version differences, and update notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to browse public Sogou pages and summarize download, help, privacy, and version information, which can become outdated or vary by platform.

Mitigation: Use official Sogou public pages as the source of truth, cite the relevant page, and state the platform and version context when summarizing.

Risk: Users could confuse public-information guidance with permission to install software, access private files, or change device settings.

Mitigation: Keep outputs limited to public information and do not request credentials, private data, device access, or system changes.

## Reference(s):

- [Sogou Input Method homepage](https://shurufa.sogou.com/)
- [ClawHub Sogou skill page](https://clawhub.ai/codekungfu/skills/sogou)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown summaries and structured lists with official links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should distinguish Android, iOS, Windows, and macOS information when platform differences matter.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
