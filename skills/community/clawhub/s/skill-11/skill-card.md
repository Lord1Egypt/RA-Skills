## Description:

Agent Reach helps agents search, read, and interact with web and social platforms including Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, WeChat Articles, LinkedIn, Boss Zhipin, RSS, Exa web search, and arbitrary web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raiway](https://clawhub.ai/user/raiway)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill when an agent needs to search online, read platform content, interact with supported social and web services, or configure access to those channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents broad authority across web and social-platform automation, including account-connected actions.

Mitigation: Install only when this authority is acceptable, use secondary accounts and dedicated browser profiles, and require explicit confirmation before posting or commenting.

Risk: Some supported channels rely on cookies, login state, proxy configuration, or anti-bot bypass paths.

Mitigation: Review setup commands before execution, avoid casual storage of primary-account cookies, and use anti-bot bypass paths only when platform and account risks are accepted.

## Reference(s):

- [Agent Reach install guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific commands, setup guidance, search results, page summaries, transcripts, and posting or commenting instructions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
