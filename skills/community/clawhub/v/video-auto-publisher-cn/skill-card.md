## Description:

Automates video publishing to Bilibili, Douyin, and Xiaohongshu using Playwright browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huanghonggit](https://clawhub.ai/user/huanghonggit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to automate browser-based upload, metadata entry, and publishing workflows for videos on major Chinese creator platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable account sessions are stored in plaintext local cookie files.

Mitigation: Use only accounts you control, restrict file access to the cookies directory, and do not store or share generated session files.

Risk: Commands may immediately upload and publish public video content with generated defaults.

Mitigation: Review the selected video, title, description, tags, and target platforms before execution; require an explicit operator approval outside the skill before posting.

Risk: The artifact claims anti-detection behavior and depends on changing creator-platform web interfaces.

Mitigation: Confirm the workflow complies with each platform's rules and re-test selectors in a controlled account before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huanghonggit/skills/video-auto-publisher-cn)
- [Publisher profile](https://clawhub.ai/user/huanghonggit)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [CLI log text with command-line arguments and local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload and publish public video content, write logs, and store reusable platform sessions locally.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
