## Description:

Plans, drafts, humanizes, formats, and saves WeChat public account articles to a configured account's draft box.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjiahui11](https://clawhub.ai/user/chenjiahui11)

### License/Terms of Use:

MIT-0

## Use Case:

External publishers and content operators use this skill to plan, draft, humanize, format, and save WeChat public account articles as drafts in a configured WeChat account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The license gate sends a stable device fingerprint and license key to a default plaintext HTTP licensing server.

Mitigation: Use the skill only when the publisher and licensing server are trusted, prefer an HTTPS license endpoint through TMO_LICENSE_SERVER, and avoid sharing reusable card keys.

Risk: The license key is saved locally in plaintext for reuse.

Mitigation: Restrict access to the local license file and rotate or revoke any card key that may have been exposed.

Risk: The workflow can create drafts in a connected WeChat public account using configured app credentials.

Mitigation: Protect WeChat app credentials and verify the selected account and draft content before publishing or allowing external writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenjiahui11/skills/weixin-wechat-channel)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown article content, command snippets, and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a WeChat public account draft and return a Media ID after credentialed execution.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
