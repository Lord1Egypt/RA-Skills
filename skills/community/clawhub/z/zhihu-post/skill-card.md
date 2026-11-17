## Description:

在知乎发布内容（专栏文章、想法/动态），使用 Chrome Browser Relay 控制用户的 Chrome 浏览器完成发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[inuyashayang](https://clawhub.ai/user/inuyashayang)

### License/Terms of Use:

MIT

## Use Case:

External users and creators use this skill to prepare and publish Zhihu column articles or short posts from an attached, logged-in Chrome browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content through a logged-in Zhihu browser session without a strong final confirmation gate.

Mitigation: Keep the target tab visible, review the exact title and body, and require explicit final confirmation before any publish button is clicked.

Risk: Generated HTML from the helper script may include unsafe or unintended markup.

Mitigation: Treat generated HTML as untrusted unless it has been reviewed and sanitized before posting.

## Reference(s):

- [知乎 DOM 选择器速查](references/dom-selectors.md)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Zhihu column editor](https://zhuanlan.zhihu.com/write)
- [Zhihu](https://www.zhihu.com/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown guidance with inline browser commands, JavaScript snippets, and JSON helper-script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script validates title and content length and can convert simple Markdown to Zhihu-friendly HTML.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
