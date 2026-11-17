## Description:

Automates Zhihu article publishing by guiding an agent through Chrome-based login, drafting, formatting, and publication with xbrowser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuxucai](https://clawhub.ai/user/liuxucai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to automate publishing prepared articles to Zhihu through a controlled Chrome browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Zhihu account credentials could be exposed if they are supplied through command-line text.

Mitigation: Prefer manual login or an isolated browser profile, and do not provide passwords through command-line text.

Risk: The skill can publish unintended content to a live Zhihu account.

Mitigation: Use it only for deliberate publishing requests and require a preview plus explicit confirmation before publication.

Risk: Article text copied from untrusted sources may be unsafe for browser-based insertion.

Mitigation: Avoid untrusted article text unless the insertion method is changed to treat content strictly as data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuxucai/skills/zhihu-publisher)
- [Zhihu Sign-In](https://www.zhihu.com/signin)
- [Zhihu Article Editor](https://zhuanlan.zhihu.com/write)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Chrome and xbrowser; article text is inserted in chunks for long drafts.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
