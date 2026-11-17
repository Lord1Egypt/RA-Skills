## Description:

Automates a restaurant visit note workflow by generating an AI visit image, collecting recommended dish images from a review link, drafting promotional copy, and publishing the result to Tencent Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turkyden](https://clawhub.ai/user/turkyden)

### License/Terms of Use:

MIT-0

## Use Case:

Restaurant brand operators and content production teams use this skill to assemble promotional visit notes from store imagery, review links, generated text, and Tencent Docs publishing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary says the skill uses hidden Tencent Docs credentials.

Mitigation: Replace hidden credential access with an explicit least-privilege token or documented authorization flow before installation or use.

Risk: The authoritative security summary says the skill grants public edit access to generated Tencent Docs.

Mitigation: Default published documents to private or view-only sharing and require explicit user confirmation before enabling public editing.

Risk: The authoritative security guidance cites deceptive first-person review claims and automated restaurant review-style content.

Mitigation: Require disclosure and human review of generated promotional copy, and avoid claims that imply personal experience unless they are user-provided and true.

Risk: The authoritative security guidance cites uploading local images and generated text, plus python3 -c injection and /tmp file-handling issues.

Mitigation: Use only licensed or user-provided images, sanitize shell/Python inputs, and replace shared /tmp paths with securely created temporary files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/turkyden/skills/xiaofeng-skills)
- [Tencent Docs MCP endpoint](https://docs.qq.com/openapi/mcp)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Configuration instructions]

**Output Format:** [Markdown content, generated image/document assets, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REPLICATE_API_TOKEN and the tencent-docs and tandian-image-skills dependencies.]

## Skill Version(s):

1.1.10 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
