## Description:

Automates posting content with images to LinkedIn, X/Twitter, Facebook, WordPress, and Substack via browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quoc-modoro](https://clawhub.ai/user/quoc-modoro)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, creators, and developers use this skill to publish prepared posts and images across multiple social and publishing platforms, then verify that the posts were published successfully.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish directly to live public accounts.

Mitigation: Confirm each selected platform and the final post content before publishing, and use only accounts approved for agent-assisted posting.

Risk: WordPress credentials are stored in a plaintext .env file.

Mitigation: Use a least-privileged WordPress account, protect the credential file, and rotate or replace credentials if exposure is suspected.

Risk: Draft media or session state from previous posts may be reused or deleted by mistake.

Mitigation: Verify queued images, open drafts, and platform upload state before deleting media or submitting a post.

## Reference(s):

- [ARM Upload Guide](references/arm-upload-guide.md)
- [Platform Quirks & Gotchas](references/platform-quirks.md)
- [ClawHub Skill Page](https://clawhub.ai/quoc-modoro/skills/social-auto-poster)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown instructions with inline shell commands, browser workflow steps, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces platform-specific posting steps and verification checks; it does not read feeds, direct messages, analytics, or schedule posts.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
