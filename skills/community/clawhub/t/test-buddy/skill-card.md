## Description:

Buddy generates a deterministic local pet gacha result for a provided name or the local user name, including rarity, species, stats, shiny status, and accessories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subcoldzhang](https://clawhub.ai/user/subcoldzhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as a local toy gacha experience that prints a deterministic Buddy pet card for a supplied name. It is suitable for lightweight entertainment or testing agent workflows that invoke a Python command-line script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script defaults to the local user name when no explicit name is supplied.

Mitigation: Pass an explicit name when the local account name should not appear in output.

Risk: The interface and generated card text are written primarily in Chinese.

Mitigation: Confirm the language is appropriate for the target users before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subcoldzhang/skills/test-buddy)
- [Publisher profile](https://clawhub.ai/user/subcoldzhang)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text pet card printed by a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic output for the same input name; defaults to local user-name environment variables when no name is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
