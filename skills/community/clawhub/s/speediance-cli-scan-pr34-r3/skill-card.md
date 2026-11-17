## Description:

Read Speediance workout data, browse and export the exercise catalog, and create custom training programs through the Speediance cloud API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stozo04](https://clawhub.ai/user/stozo04)

### License/Terms of Use:

MIT-0

## Use Case:

Speediance users can use an agent to retrieve completed workout details, browse exercises, and prepare custom programs for their own Gym Monster account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports a permissions mismatch and incomplete reference resolution, with medium confidence.

Mitigation: Review the requested access against the commands you plan to use and check unresolved references before enabling the skill.

Risk: The CLI can store an account password in config.json as plain JSON.

Mitigation: Prefer environment variables backed by a secret store when practical, protect the config file, and never commit it.

## Reference(s):

- [Project repository](https://github.com/stozo04/speediance-cli)
- [ClawHub skill listing](https://clawhub.ai/stozo04/skills/speediance-cli-scan-pr34-r3)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Structured JSON data and shell commands with setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workout and exercise data are returned as structured output; program creation uses a plan supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
