## Description:

ZM 选题策略与内容审核用于自媒体内容的选题判断、观点提炼、结构设计、初稿审查、改稿方向、用户目标匹配和发布风险判断。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and editorial teams use this Chinese-first skill to assess self-media topics, sharpen viewpoints, design platform-specific structures, review drafts, and identify concrete revision or publication risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Editorial recommendations may affect publication quality, brand positioning, or commercial messaging.

Mitigation: Use the skill's PASS / NEEDS_REVISION / BLOCKED result as editorial guidance and keep human review before publication.

Risk: The skill is Chinese-first and focused on self-media strategy, so multilingual or general-purpose writing tasks may be a poor fit.

Mitigation: Ask explicitly for another language or adapt the prompts when using it outside Chinese self-media editorial review.

Risk: Content advice can still produce overclaiming, compliance, or AI-flavored language issues.

Mitigation: Apply the bundled checks for compliance boundaries, exaggerated claims, concrete scenes, and required revision items before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-editorial-strategy-review)
- [最小必填字段｜选题策略与内容审核](artifact/templates/minimum_required_fields.md)
- [AI 可执行性审核表｜编辑审核](artifact/checklists/ai_readiness_checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review with scoring, structured recommendations, and a PASS / NEEDS_REVISION / BLOCKED decision.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first editorial review; no executable code, network access, credential handling, or persistence.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
