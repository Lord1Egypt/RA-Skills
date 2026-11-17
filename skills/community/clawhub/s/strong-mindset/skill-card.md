## Description:

Strong Mindset is a Chinese-language coaching skill for reframing user concerns, evaluating mindset-oriented writing, running a 7-question score, drafting articles, and polishing drafts with a direct "strong mindset" style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forrestneo](https://clawhub.ai/user/forrestneo)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for Chinese-language mindset coaching, actionable advice, text assessment, short self-assessment reports, article generation, and draft refinement. The skill is most useful when a user brings a concrete dilemma, self-doubt, relationship friction, or a draft that should be rewritten in the strong-mindset voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted report metadata may introduce unescaped HTML or JavaScript into generated HTML reports.

Mitigation: Use trusted or reviewed report JSON only, validate or escape report metadata before generation, and review generated HTML before sharing.

Risk: The skill uses a subjective coaching and assessment framework that may not fit every user or decision context.

Mitigation: Treat outputs as guidance and writing support, not as authoritative psychological, legal, medical, financial, or employment advice.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/forrestneo/strong-mindset/tree/main/strong-mindset)
- [ClawHub skill page](https://clawhub.ai/forrestneo/skills/strong-mindset)
- [Skill definition](SKILL.md)
- [Core style guide](references/style-guide.md)
- [Article corpus guide](references/articles/README.md)
- [HTML report generator](references/generate_report.py)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Chinese-language prose, Markdown responses, and optional single-file HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bundled style guidance, article references, and a local standard-library report generator when producing assessment or quiz reports.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
