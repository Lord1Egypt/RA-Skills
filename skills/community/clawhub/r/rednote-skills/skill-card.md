## Description:

Comprehensive tool for interacting with the Rednote (Xiaohongshu) platform by searching posts, extracting note content as markdown, and performing account actions such as liking, commenting, collecting, following, and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrmao007](https://clawhub.ai/user/mrmao007)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to automate Rednote content discovery, note extraction, and authenticated engagement workflows through browser automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a logged-in Xiaohongshu account to like, comment, collect, follow, and publish content without strong per-action safeguards.

Mitigation: Review each account action before execution and prefer adding URL allowlisting, dry-run behavior, or explicit confirmations before using the skill with a real account.

Risk: The skill stores the Xiaohongshu browser session in rednote_cookies.json.

Mitigation: Treat rednote_cookies.json like a password, keep it out of shared folders and source control, and use protected storage where possible.

Risk: Automated public engagement may affect the user's account reputation or platform compliance posture.

Mitigation: Use the skill only for intended, reviewed interactions and follow Xiaohongshu's terms, community rules, and rate limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrmao007/skills/rednote-skills)
- [Rednote / Xiaohongshu website](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Rednote note URLs, extracted note markdown, and success or error status messages for authenticated account actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
