## Description:

Complete toolkit for publishing content to Xiaohongshu (小红书), including automated browser control, image generation, content formatting, and a publishing pipeline for OpenClaw browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siaslfs](https://clawhub.ai/user/siaslfs)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to prepare and publish Xiaohongshu image-text posts through OpenClaw, including browser navigation, cover generation, uploads, title and body entry, and login-session checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content through a live Xiaohongshu account.

Mitigation: Use a dedicated or test account where possible and review all titles, body text, images, and target account state before allowing publication.

Risk: The security summary identifies unsafe shell execution and warns against untrusted titles, content, and filenames.

Mitigation: Do not pass untrusted input to the scripts; quote, validate, or sanitize titles, content, image paths, and filenames before execution.

Risk: The skill can maintain recurring browser access through cron, daemon mode, and browser-session backup or restore behavior.

Mitigation: Enable keepalive only when recurring access to the logged-in browser is acceptable, and clear the OpenClaw browser profile and session backup when the skill is no longer used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/siaslfs/skills/xiaohongshu-publish-kit)
- [Xiaohongshu creator platform](https://creator.xiaohongshu.com)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser automation instructions and helper script usage for Xiaohongshu publishing workflows.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
