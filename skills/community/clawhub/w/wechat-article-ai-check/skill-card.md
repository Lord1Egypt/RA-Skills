## Description:

Reviews WeChat public-account articles for originality, substantive value, homogeneity, low-value AIGC signals, formatting quality, and platform-risk claims, then gives evidence-based improvement guidance or a confirmed rewrite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT

## Use Case:

External creators, editors, and publishing teams use this skill to review WeChat article drafts for originality, information value, text-risk signals, and mobile-readable structure. After the initial assessment, they can ask the agent to rewrite the article while preserving supplied facts and avoiding fabricated evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Platform-rule and source-comparison conclusions can be uncertain without supplied rules, reliable sources, or web access.

Mitigation: Require the user to provide original rules or sources, use web search only when explicitly requested, cite checked sources, and mark unsupported conclusions as unable to determine.

Risk: Rewrite requests can introduce unsupported cases, data, quotes, people, interviews, or citations.

Mitigation: Use supplied material as the factual boundary, ask for missing evidence, insert clear placeholders for required source material, or remove unsupported claims.

Risk: Manual clone-and-copy installation can install files outside the reviewed release if the source is not checked.

Mitigation: Install from the reviewed ClawHub release when possible, and review the copied files and hashes before enabling the skill in an agent.

## Reference(s):

- [README](README.md)
- [Changelog](CHANGELOG.md)
- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/wechat-article-ai-check)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured findings, tables, checklists, and rewrite drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is designed as a two-stage workflow: review and recommendations first, then a full rewrite only after user confirmation.]

## Skill Version(s):

1.0.0 (source: SKILL.md, CHANGELOG.md released 2026-07-29, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
