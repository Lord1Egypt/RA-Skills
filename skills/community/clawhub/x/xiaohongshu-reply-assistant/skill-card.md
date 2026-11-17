## Description:

小红书智能回复助手 analyzes Xiaohongshu comments for sentiment and intent, generates personalized reply suggestions, manages comment history and batch processing, and can optionally monitor notes through Xiaohongshu API access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoliuzhuan](https://clawhub.ai/user/xiaoliuzhuan)

### License/Terms of Use:

MIT

## Use Case:

Content creators, brand operations teams, MCN agencies, and developers use this skill to triage Xiaohongshu comments, draft response options, process comment batches, and review activity before posting replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle Xiaohongshu session or API credentials when API integration is used.

Mitigation: Prefer offline analysis when possible, provide credentials only to trusted integration paths, and avoid sharing session cookies with unreviewed code.

Risk: The documented dependency installation command is not pinned or hash verified.

Mitigation: Install in an isolated environment and use pinned, hash-verified dependency files before production use.

Risk: Generated replies may be inaccurate, inappropriate, or non-compliant with platform or legal requirements.

Mitigation: Review suggested replies before posting and follow Xiaohongshu platform rules and applicable privacy obligations.

## Reference(s):

- [xiaohongshu-mcp API access reference](https://github.com/xpzouying/xiaohongshu-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples, JSON configuration snippets, and generated reply text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce multiple suggested replies per comment and local configuration or history file guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
