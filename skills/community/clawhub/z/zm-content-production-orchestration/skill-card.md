## Description:

ZM 图文内容生产编排用于公众号、小红书、抖音等图文内容的多 Agent 生产流程，覆盖选题定位、正文生产、视觉生产、审核返工、排版发布和交付包归档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams, creators, and agent operators use this skill to coordinate article, social post, cover image, review, revision, publishing-prep, and delivery-package workflows for Chinese-language content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated content or image direction may be inaccurate, unsuitable for the target platform, or not ready for publication.

Mitigation: Review the generated article, image, score, checklist, and delivery package before publishing or sharing externally.

Risk: The workflow creates local deliverable files and may place content in an unintended output path.

Mitigation: Confirm the requested output path and inspect generated files before archiving or distributing the package.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-content-production-orchestration)
- [Publisher profile](https://clawhub.ai/user/jerryxn)
- [AI readiness checklist](artifact/checklists/ai_readiness_checklist.md)
- [Minimum required fields](artifact/templates/minimum_required_fields.md)
- [Subagent execution prompt](artifact/templates/subagent_execution_prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown, HTML preview files, image deliverables, JSON metadata, and checklist files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local deliverable packages under an outputs/YYYY-MM-DD-topic/ path when followed by an agent.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
