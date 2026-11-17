## Description:

Builds auditable writing profiles for X accounts from complete public posts and articles, supporting separate short- and long-form analysis and evidence-linked writing practice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and researchers use this skill to study a selected X author's public posts or articles, audit the collected works, and develop evidence-linked writing methods without copying the author's identity or experiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Collection could expose private or session data if the agent uses unauthorized access.

Mitigation: Use only an authorized browser or official API for user-selected public accounts; avoid private messages, credentials, and session data.

Risk: Local corpus and audit files could overwrite existing work.

Mitigation: Choose a fresh output directory for each audit and review file destinations before writing.

Risk: Incomplete or unverified samples could make writing profiles misleading.

Mitigation: Confirm source identity and complete works, distinguish posts from articles, and report missing branches and sampling limits explicitly.

## Reference(s):

- [X Writing DNA on ClawHub](https://clawhub.ai/0xcjl/skills/x-writing-dna)
- [Collection guidance](references/collection.md)
- [Analysis guidance](references/analysis.md)
- [Writing DNA concept inspiration](https://github.com/larashero3-dotcom/writing-dna-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV]

**Output Format:** [Markdown profiles and status reports, with JSONL corpus records and JSON/CSV audits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separate post and article profiles include source-work evidence, limitations, and practice actions; incomplete collection is reported as partial.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
