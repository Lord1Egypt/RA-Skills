## Description:

Reads and searches a user's own desktop WeChat data, masks common personal identifiers, and supplies message data for summaries and optional delivery workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gp198922](https://clawhub.ai/user/gp198922)

### License/Terms of Use:

MIT-0

## Use Case:

External users can query or export data from their own logged-in desktop WeChat account and prepare masked daily work briefs. The documented workflow supports Windows and Linux, requires additional setup on macOS, and does not support mobile WeChat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat content, key files, and decrypted caches can expose sensitive data if left unmasked, shared, or synced.

Mitigation: Use masking before export or delivery, restrict access to key and cache files, avoid sharing or syncing them, and clear decrypted caches when finished.

Risk: The documented workflow can send summaries to email, a WeChat bot, or an HTTP endpoint despite local-only assurances.

Mitigation: Review the selected destination and the content being sent; remove sensitive details before delivery and use only destinations you control and trust.

Risk: Setup may require elevated process access or changes to WeChat signing and debugging protections.

Mitigation: Review the setup steps and requested permissions before running them, and proceed only if you accept those changes.

Risk: The security scan was incomplete, with one degraded analysis and unresolved references.

Mitigation: Treat the scan as incomplete and review the reported data-access and delivery behavior before installing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gp198922/skills/wechat-local-reader-publish)
- [TANGandXUE/wcdb-key-tool](https://github.com/TANGandXUE/wcdb-key-tool)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Guidance]

**Output Format:** [JSON command output, Markdown exports and summaries, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional masking of phone numbers, identity numbers, bank card numbers, and email addresses; source chat data may remain unredacted unless masking is enabled.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
