## Description:

Read Speediance workouts, browse the exercise catalog, and create custom training programs for a Gym Monster machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stozo04](https://clawhub.ai/user/stozo04)

### License/Terms of Use:

MIT-0

## Use Case:

External Speediance users and compatible agents use this skill to review workout history, inspect available exercises, and create training programs on the user's machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account credentials and a live session token; config files may contain a plaintext password.

Mitigation: Prefer exported environment variables, protect local credential and token files, and never commit them.

Risk: The skill accesses personal workout data through the Speediance cloud API and can create programs on the user's account.

Mitigation: Use your own account, review workout data before sharing it, and run `push --dry-run` before creating a program.

Risk: The partial security scan did not establish runtime permissions and noted an unresolved shell-permission mismatch.

Mitigation: Review the skill's requested network, file, and shell access before installing or using it.

## Reference(s):

- [Speediance CLI project homepage](https://github.com/stozo04/speediance-cli)
- [ClawHub skill page](https://clawhub.ai/stozo04/skills/speediance-cli-scan-pr34-r2)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON workout, session, and exercise data with command-line usage instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create a training program in the user's Speediance account; Gym Monster v1 is tested, while Gym Monster 2 is untested.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
