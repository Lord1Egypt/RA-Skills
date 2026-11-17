## Description:

文章品鉴师 - 多维度评估文章质量、检测AI味/大便味、识别原创内容

This skill is ready for commercial/non-commercial use.

## Publisher:

[forealmy](https://clawhub.ai/user/forealmy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content reviewers use this skill to classify Chinese articles, assess article quality, estimate reading value, and generate AI/originality heuristics before deciding whether to read or review a piece.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI and originality results may be mistaken for proof of authorship or content quality.

Mitigation: Treat the results as heuristic opinions and keep human review in the decision loop.

Risk: Shared deployments that accept arbitrary large submissions may face reliability or abuse issues.

Mitigation: Use local installation for normal article scoring or enforce input limits before offering it as a shared service.

Risk: Unpinned dependencies can change behavior over time.

Mitigation: Pin and review dependencies before production use.

Risk: Generated Markdown could expose unsafe rendering behavior in downstream viewers.

Mitigation: Render generated Markdown with raw HTML and remote resource loading disabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forealmy/skills/tmp70s6amg4)
- [Skill instructions](artifact/SKILL.md)
- [Scoring weights](artifact/config/scoring_weights.json)
- [AI exemption rules](artifact/config/exemption_rules.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON reports, Markdown summaries, command-line text, and Python analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces heuristic article quality scores, type labels, reading advice, and AI/originality indicators for supplied article text.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
