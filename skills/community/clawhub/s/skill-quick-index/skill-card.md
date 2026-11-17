## Description:

Build a wide-trigger, precise-match index for local OpenClaw skills (L1-L3), then quickly route by intent/category/keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to look up local skills from natural-language requests and route those requests to matching L1-L3 skills by category, keyword, and trigger priority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad natural-language matches may recommend powerful skills for messaging, automation, configuration changes, skill installation, or agent evolution without clear confirmation boundaries.

Mitigation: Treat lookup results as suggestions only and require explicit user confirmation before invoking or installing any recommended high-impact skill.

Risk: The local index can become stale or domain-specific, causing incomplete or misleading recommendations.

Mitigation: Review and maintain index/skill_index.json before relying on routing results for operational workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halfmoon82/skills/skill-quick-index)
- [Publisher profile](https://clawhub.ai/user/halfmoon82)
- [Manifest homepage](https://clawhub.ai/halfmoon82/skill-quick-index)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup results rank recommended skills and categories by score.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, clawhub.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
