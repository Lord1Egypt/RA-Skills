## Description:

Read body metrics from a Wyze smart scale, including weight, BMI, body fat, water, muscle, and BMR, with support for multiple household members through the unofficial wyze-node client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noelportugal](https://clawhub.ai/user/noelportugal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve recent Wyze smart-scale readings, weigh-in history, and household member identifiers for private body-metric questions and trend checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Wyze API credentials, cached login tokens, household member identifiers, and body-composition records.

Mitigation: Keep WYZE_ENV and token files private, run the skill only in private sessions, and share readings only with the scale user.

Risk: The runtime dependency is declared with a version range for wyze-node.

Mitigation: Pin wyze-node with a lockfile before use and review dependency updates before installing them.

Risk: The skill depends on unofficial Wyze API behavior that may change.

Mitigation: Recheck authentication and scale-reading behavior after Wyze API or wyze-node changes, and refresh the cached token when auth errors occur.

## Reference(s):

- [wyze-node GitHub repository](https://github.com/noelportugal/wyze-node)
- [wyze-node npm package](https://www.npmjs.com/package/wyze-node)
- [Wyze developer API key console](https://developer-api-console.wyze.com/#/apikey/view)
- [ClawHub skill page](https://clawhub.ai/noelportugal/skills/wyze-scale)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive body-composition records, dates, user names, and household member identifiers.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
