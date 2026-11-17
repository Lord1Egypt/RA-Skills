## Description:

Fetch a public WeChat article URL, archive the raw HTML, and convert the article into a stage-1 compatible brief in `content-production/inbox/`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abigale-cyber](https://clawhub.ai/user/abigale-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content workflow operators use this skill to collect a publicly reachable WeChat article from a `mp.weixin.qq.com` URL, extract article metadata and candidate body text, and prepare a reusable brief for downstream writing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts user-supplied external URLs without an artifact-backed allowlist.

Mitigation: Use trusted public WeChat article URLs and avoid feeding arbitrary links.

Risk: The skill preserves untrusted article text and raw HTML for downstream agent workflows.

Mitigation: Review generated briefs before passing them to other agents because source article text may contain misleading instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abigale-cyber/skills/wechat-collect)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown brief plus archived HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a stage-1 compatible brief under `content-production/inbox/` and raw article HTML under `content-production/inbox/raw/wechat/`.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
