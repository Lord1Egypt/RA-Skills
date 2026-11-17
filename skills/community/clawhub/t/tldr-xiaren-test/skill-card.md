## Description:

Simplified man pages from tldr-pages. Use this to quickly understand CLI tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuji10000qian-svg](https://clawhub.ai/user/liuji10000qian-svg)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to have agents consult concise tldr command examples before falling back to longer CLI manuals or help output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refreshing the local tldr cache may use network access depending on the installed tldr client.

Mitigation: Only run `tldr --update` when cache refresh is acceptable for the current environment.

Risk: Concise examples may omit edge cases or safety warnings present in full manuals.

Mitigation: Fall back to `man` or `--help` when tldr lacks the needed command detail.

## Reference(s):

- [tldr-pages](https://github.com/tldr-pages/tldr)
- [ClawHub skill page](https://clawhub.ai/liuji10000qian-svg/skills/tldr-xiaren-test)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend refreshing the local tldr cache when command examples are missing.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
