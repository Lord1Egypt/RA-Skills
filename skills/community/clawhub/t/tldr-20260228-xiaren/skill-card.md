## Description:

Simplified man pages from tldr-pages. Use this to quickly understand CLI tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuji10000qian-svg](https://clawhub.ai/user/liuji10000qian-svg)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to ask an agent for concise CLI command examples from local tldr pages before falling back to full manuals or help output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local tldr cache may be stale or missing entries, and cache refreshes may require network access depending on the installed tldr client.

Mitigation: Confirm the tldr client is installed and allow `tldr --update` only when a cache refresh is acceptable for the environment.

Risk: Concise examples may omit edge cases or command-specific safety details.

Mitigation: Use `man` or `--help` when tldr output is unavailable or when complete option semantics are needed before running a command.

## Reference(s):

- [tldr-pages project](https://github.com/tldr-pages/tldr)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local tldr client; cache updates may require network access depending on the installed client.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
