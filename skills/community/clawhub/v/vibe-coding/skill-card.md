## Description:

Build software with AI by describing what you want, with guidance on prompting techniques, workflow patterns, rules files, and when to intervene.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and builders use this skill for practical guidance on AI-assisted software creation, including prompt framing, research-plan-implement workflows, persistent rules files, tool selection, testing, and security review boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may delegate security-sensitive implementation, including auth, payments, permissions, schemas, secrets, or user data handling, without enough human review.

Mitigation: Use the skill's guidance to review plans and diffs, run tests, and manually scrutinize sensitive code paths before accepting generated changes.

Risk: The skill provides general AI-assisted coding guidance and does not execute or validate code itself.

Mitigation: Treat outputs as advice; verify generated changes through testing, manual review, and behavior checks before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/vibe-coding)
- [Prompting techniques](artifact/prompting.md)
- [Research-plan-implement workflow](artifact/workflow.md)
- [Rules files configuration](artifact/rules-files.md)
- [Common pitfalls and fixes](artifact/pitfalls.md)
- [Vibe coding tools by use case](artifact/tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with examples and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external tools, credentials, or runtime execution are required by the skill itself.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
