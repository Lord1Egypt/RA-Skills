## Description:

Processes WeChat public account article links by fetching pages from mp.weixin.qq.com/s/ and extracting article text for the agent to use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alienhub](https://clawhub.ai/user/alienhub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve readable text from WeChat public article URLs when a conversation includes an mp.weixin.qq.com/s/ link or a request to fetch a WeChat article.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetch script performs outbound web requests and server security evidence notes that it can fetch arbitrary URLs.

Mitigation: Use the skill only for intended mp.weixin.qq.com/s/ article links and prefer a version that validates allowed hosts, blocks local or private destinations, and rejects unsafe redirects.

Risk: Server security evidence notes that response handling is not bounded.

Mitigation: Run in a constrained environment and prefer a version that caps response size, keeps timeouts, and limits retries.

Risk: Dependencies are declared with lower bounds but are not pinned.

Mitigation: Pin and review dependencies before deployment in environments that require reproducible builds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alienhub/skills/wechat-article-skill)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text article content with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return stderr guidance recommending browser fallback when direct fetching fails.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
