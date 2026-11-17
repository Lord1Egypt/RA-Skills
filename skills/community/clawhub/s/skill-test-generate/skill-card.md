## Description:

Generates structured SFT-level functional test cases for Agent Skills in JSON format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyifm](https://clawhub.ai/user/liyifm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent evaluators use this skill to generate functional test cases for Agent Skills, including routing, workflow, instruction clarity, and exception or security scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads all non-hidden files in a target skill directory or extracted ZIP while generating line-referenced tests.

Mitigation: Use it only with trusted skill directories or ZIP files.

Risk: The skill writes the generated JSON to a user-selected output path.

Mitigation: Choose an output path that is safe for the agent to create or overwrite.

## Reference(s):

- [Skill Test Generate release](https://clawhub.ai/liyifm/skills/skill-test-generate)
- [Agent Skills specification](https://agentskills.io/specification)
- [Test schema reference](references/test-schema.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Structured JSON test-case files with validation feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validated outputs include generated summary counts and a verified flag.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
