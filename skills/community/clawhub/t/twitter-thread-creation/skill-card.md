## Description:

Twitter/X thread writing with hook tweets, thread structure, and engagement optimization, including tweet formatting, character limits, media attachments, and posting strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

External creators, marketers, and social media operators use this skill to draft, structure, format, and optionally post Twitter/X threads with hooks, media guidance, and engagement tactics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick start asks users to install a CLI through a mutable remote shell script.

Mitigation: Prefer a manual, version-pinned installation path and verify downloaded binaries against published checksums before use.

Risk: The skill can generate commands that post content through an authenticated X account.

Mitigation: Review generated tweet text, account context, and command inputs before executing any posting command.

Risk: Related-skill examples use npx commands that install separate packages outside this skill.

Mitigation: Treat each related-skill install as a separate dependency requiring its own source, version, and security review.

## Reference(s):

- [Inference.sh](https://inference.sh)
- [Inference.sh CLI installer](https://cli.inference.sh)
- [Inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tweet text examples and inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Twitter/X post text, thread structure, media suggestions, and infsh CLI commands.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
