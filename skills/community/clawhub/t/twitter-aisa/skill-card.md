## Description:

Twitter/X command center for research, monitoring, watchlists, and approved posting through AIsa.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to research Twitter/X activity, monitor watchlists and trends, inspect profiles and conversations, and publish approved posts through OAuth without sharing passwords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The posting helper can expose the AIsa API key in command output.

Mitigation: Use only a revocable AISA_API_KEY, avoid posting helper workflows until raw-key output is fixed, and rotate any key that may have appeared in logs or agent transcripts.

Risk: Media uploads can read local files without enforcing a workspace boundary.

Mitigation: Only pass explicitly approved workspace media paths and avoid media upload workflows until a workspace-boundary check is added.

Risk: Twitter queries, post text, OAuth requests, and approved media uploads are sent through api.aisa.one.

Mitigation: Review data sharing expectations before installation and use the skill only when relay-based Twitter/X workflows are acceptable.

## Reference(s):

- [AIsa Twitter OAuth](references/post_twitter.md)
- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/twitter-aisa)
- [AIsa homepage](https://aisa.one)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; read, OAuth, posting, and approved media upload requests are relayed through api.aisa.one.]

## Skill Version(s):

1.0.5 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
