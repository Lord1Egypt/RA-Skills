## Description:

Fetches WeChat public account articles from mp.weixin.qq.com links and saves article metadata, body text, image links, and video links as Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[limingfa](https://clawhub.ai/user/limingfa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and archivists use this skill to convert WeChat public account articles into local Markdown files with source metadata and media references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch any user-supplied URL even though its documented scope is WeChat public account articles.

Mitigation: Use only trusted mp.weixin.qq.com article links and run the skill in an environment with constrained outbound network access.

Risk: The skill writes generated Markdown files to a local output directory.

Mitigation: Run it in a workspace where local file writes are expected and review the selected output directory before execution.

Risk: The --images option is documented, but local image download should not be relied on for archival completeness.

Mitigation: Treat generated image entries as remote links unless image preservation is verified separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/limingfa/skills/wechat-mp-reader-fzx)

## Skill Output:

**Output Type(s):** [markdown, json, text, shell commands, code]

**Output Format:** [Markdown files with article metadata, optional JSON metadata, and command-line or Python API output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes Markdown files locally; image references remain remote WeChat CDN links unless separately handled.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
