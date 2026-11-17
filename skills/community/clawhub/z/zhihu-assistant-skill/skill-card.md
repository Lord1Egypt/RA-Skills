## Description:

知乎热榜抓取与回答草稿生成助手 - 自动抓取知乎热榜，使用 AI 生成优质回答草稿，推送到飞书审核

This skill is ready for commercial/non-commercial use.

## Publisher:

[naivekid](https://clawhub.ai/user/naivekid)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to fetch Zhihu hot-list questions, generate AI-assisted answer drafts, track an audit queue, and prepare Feishu review notifications before any manual publishing step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Zhihu session cookies and AI provider API keys.

Mitigation: Treat the cookie and API keys as secrets, configure them only through trusted secret/config storage, avoid committing them, and rotate them if exposed.

Risk: The config display path may expose sensitive configuration if redaction is not confirmed.

Mitigation: Do not use the config display command until secret redaction has been verified in the target OpenClaw environment.

Risk: The installer creates local commands and installs Python dependencies.

Mitigation: Review the installer before use, run it without elevated privileges in a dedicated environment, and pin dependencies where operational policy requires reproducibility.

Risk: Generated answers may be inaccurate, policy-violating, or unsuitable for publication.

Mitigation: Keep generated answers in the review queue and require human review against Zhihu community rules before posting.

Risk: The skill sends drafted content and question metadata to configured AI and notification services.

Mitigation: Use only trusted AI endpoints and Feishu destinations, and avoid processing content that should not leave the operator's environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/naivekid/skills/zhihu-assistant-skill)
- [Publisher profile](https://clawhub.ai/user/naivekid)
- [Kimi open platform](https://platform.moonshot.cn/)
- [Zhihu hot-list API endpoint](https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total)
- [Server-resolved provenance](unavailable)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [CLI text and Markdown-formatted review messages, with JSON files for local queue and log state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates draft answer text for human review; stores pending items, status counts, and operation logs locally.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
