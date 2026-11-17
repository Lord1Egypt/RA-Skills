## Description:

Checks Markdown articles before publication to a WeChat Official Account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and publishing teams use this skill to preflight Markdown articles before posting them to WeChat Official Accounts. It checks article metadata, cover assets, image references, unsupported Obsidian image links, and unlabeled fenced code blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker reads local Markdown and asset paths supplied to it.

Mitigation: Run it only on article files and asset directories intended for inspection.

Risk: Warning-level findings may still return a passing status.

Mitigation: Review WARN output before publication, especially unsupported Obsidian image links and unlabeled fenced code blocks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoyang78/skills/wechat-preflight-check)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text check report with ERROR/WARN lines and pass/fail status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads one Markdown file and referenced local assets; no file modification is indicated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
