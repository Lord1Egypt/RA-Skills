## Description:

Manages an Eudic vocabulary notebook by generating daily vocabulary quizzes, listing saved words, and deleting mastered vocabulary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadaniya99](https://clawhub.ai/user/dadaniya99)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to create daily Eudic vocabulary quizzes from their saved word list and manage words or categories through command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Eudic API token and the security review notes unsafe token-handling guidance.

Mitigation: Use a dedicated Eudic token with the minimum permissions available and store it outside command lines or crontab entries.

Risk: The skill can delete vocabulary from a user's remote Eudic account.

Mitigation: Manually confirm word identifiers before deletion and store quiz output in a private directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dadaniya99/skills/xiaolongxia-eudic-vocab)
- [Eudic OpenAPI authorization](https://my.eudic.net/OpenAPI/Authorization)
- [Eudic OpenAPI base endpoint](https://api.frdic.com/api/open/v1)

## Skill Output:

**Output Type(s):** [text, JSON files, shell commands, configuration guidance]

**Output Format:** [Markdown-style usage guidance with shell command examples; generated quizzes and answer keys may be written as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an Eudic API token and command-line options for quiz count, output path, category, language, action, and word ID.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
