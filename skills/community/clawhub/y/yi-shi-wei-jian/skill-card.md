## Description:

Maps Chinese historical cases to present-day organizational, business, and team decisions, producing structured situation analysis, historical references, key variables, options, sandbox simulations, principles, and boundary reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greatxiaory](https://clawhub.ai/user/greatxiaory)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to turn realistic strategy or organization questions into structured Chinese-history analogy analysis. It can also help convert sourced historical cases into local JSON entries for later retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The persistent case library is under-guarded, and added cases may later influence retrieval and recommendations.

Mitigation: Review added cases before reuse and avoid storing sensitive or instruction-like text in the case library.

Risk: The CLI can write outside the stated data file when custom user case paths are supplied.

Mitigation: Do not pass custom --user-cases-path values unless you intentionally want to write that specific JSON file.

Risk: History-based sandbox analysis can be mistaken for prediction or professional advice.

Mitigation: Keep the skill's boundary reminders visible: historical analogy is not a guarantee, and high-risk legal, medical, or investment topics should receive only a structured thinking framework.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/greatxiaory/skills/yi-shi-wei-jian)
- [Project homepage](https://github.com/GreatXiaoRY/LearnFromHistory-skill)
- [Skill instructions](SKILL.md)
- [README](README.md)
- [Historical case schema](data/cases.schema.json)
- [Case submission template](examples/case_submission_template.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Structured Markdown with optional JSON case entries and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs follow fixed Chinese section headings for situation judgment, historical references, key variables, options, sandbox simulation, principles, and boundary reminders.]

## Skill Version(s):

0.1.4 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
