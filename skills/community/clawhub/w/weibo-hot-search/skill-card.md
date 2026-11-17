## Description:

Collects Weibo real-time hot search entries without a Weibo login and saves the results as a Markdown file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kazemace](https://clawhub.ai/user/kazemace)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and external users can use this skill to ask an agent to collect the public Weibo hot search ranking through a local Chrome or Edge browser session and export the captured ranking as Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that the skill points to a missing script.

Mitigation: Confirm the referenced script is included in the package before installing or running the skill.

Risk: The release evidence reports unsafe runtime guidance because the skill may use an unpinned npx fallback.

Mitigation: Use a trusted Bun installation or verify the runtime source before allowing an agent to execute the command.

Risk: The release evidence reports unsafe process-killing instructions for existing Chrome or Edge CDP processes.

Mitigation: Require user approval or verify process ownership before terminating browser processes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kazemace/skills/weibo-hot-search)
- [Weibo search page](https://weibo.com/newlogin?tabtype=search)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration]

**Output Format:** [Markdown table saved to a file, with shell command guidance for optional output path and browser settings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Chrome, Chromium, or Edge and a Bun runtime or npx fallback.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
