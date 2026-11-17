## Description:

Startup validation before you build: structured validate, compete, and mvp commands plus a reporting template for startup ideas, competitive landscape, MVP scope, and early PMF thinking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Founders, indie hackers, and startup-focused developers use this skill to structure early validation, compare competitors, and scope an MVP before building.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided startup ideas and market details may be silently recorded in the local data file.

Mitigation: Review the local data retention behavior before use, avoid entering sensitive proprietary details, and clear stored records when they are no longer needed.

Risk: The command names imply a full validation workflow, but the bundled script mainly records inputs and returns status metadata.

Mitigation: Treat command output as a workflow scaffold and require separate market research, user interviews, and competitive evidence before making business decisions.

## Reference(s):

- [Startup Validator Guide](references/startup_validator_guide.md)
- [YC: The Real Product/Market Fit](https://www.ycombinator.com/library/5z-the-real-product-market-fit)
- [Pre-build Idea Validator Use Case](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/pre-build-idea-validator.md)
- [Market Research Product Factory Use Case](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/market-research-product-factory.md)
- [Hacker News Discussion](https://news.ycombinator.com/item?id=41986396)
- [Reddit r/startups Related Thread](https://www.reddit.com/r/startups/comments/1055d61yyz/idea_validator_ai/)
- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/startup-validator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report template with JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled commands append local JSON records and return status, command, record, total_records, and reference_urls fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
