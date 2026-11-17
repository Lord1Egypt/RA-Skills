## Description:

Queries detailed nutrition data for nearly 2,000 common foods by food name, category, or specific nutrient, with search and sorting support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up food nutrition, calorie, and nutrient-ranking information through TianAPI and present the results in a readable form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Food search terms are sent to TianAPI when the lookup script or API endpoint is used.

Mitigation: Use the skill only when sharing those search terms with TianAPI is acceptable for the user and deployment context.

Risk: The TianAPI key can be exposed through command-line history, terminal logs, or a committed scripts/.env file.

Mitigation: Prefer environment variables or a secret manager, avoid passing keys on the command line, do not commit scripts/.env, and rotate exposed keys.

Risk: API quota, application approval, invalid key, or empty-result conditions can prevent a lookup from succeeding.

Mitigation: Surface TianAPI error messages clearly and direct users to check quota, API approval, key validity, and query spelling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/workxin/skills/tianapi-nutrient-query)
- [TianAPI Nutrient API documentation](https://www.tianapi.com/apiview/121)
- [TianAPI Nutrient API endpoint](https://apis.tianapi.com/nutrient/index)
- [Publisher profile](https://clawhub.ai/user/workxin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and readable nutrient lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and TIANAPI_NUTRIENT_KEY; queries are sent to TianAPI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
