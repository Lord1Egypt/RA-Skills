## Description:

Simplified man pages from tldr-pages. Use this to quickly understand CLI tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuji10000qian-svg](https://clawhub.ai/user/liuji10000qian-svg)

### License/Terms of Use:


## Use Case:

Developers and technical users use this skill to get concise examples for command-line tools before consulting longer manual pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to prefer concise tldr pages over full man pages, which may omit detailed command behavior or edge cases.

Mitigation: Use full man pages or --help output when complete option details, platform-specific behavior, or authoritative command documentation is needed.

Risk: The skill may suggest updating the local tldr cache when a page is missing.

Mitigation: Review cache update behavior against the local environment's package and network policies before running updates.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liuji10000qian-svg/skills/tldr-xiaren-test-v2)
- [tldr-pages project](https://github.com/tldr-pages/tldr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prefer concise tldr pages over full manual pages and may suggest updating the local tldr cache when a page is missing.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
