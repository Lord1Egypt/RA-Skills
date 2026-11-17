## Description:

UniSkill V4 is a minimalist AI agent framework for Socratic requirement clarification and multi-option debate recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to route ambiguous evaluation, strategy, CNC quotation, and multi-option decision requests through requirement clarification or debate-style scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt logging guidance may capture raw user inputs.

Mitigation: Remove or redact raw prompt logging before integration, especially where inputs may contain confidential or personal data.

Risk: Release automation can initialize Git, stage files, commit, tag, and push repository state.

Mitigation: Run release scripts only in an intended release repository after reviewing the exact Git operations.

Risk: Debate recommendations may rely on heuristic scoring rather than real model calls.

Mitigation: Treat recommendations as decision-support signals and validate important outcomes with real model calls, domain review, and resource limits.

Risk: Broad activation keywords can trigger the skill for ordinary evaluation or comparison requests.

Mitigation: Scope activation rules to the deployment context and require user confirmation for high-impact recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/timo2026/skills/uniskill-v4)
- [Artifact README](artifact/README.md)
- [Artifact Full README](artifact/README_FULL.md)
- [Artifact Integration Guide](artifact/INTEGRATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose, Python snippets, and structured recommendation objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include clarity questions, debate recommendations, confidence scores, setup commands, and integration guidance.]

## Skill Version(s):

4.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
