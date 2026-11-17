## Description:

Verifies ClawHub publish flows from the TypeScript client with a non-trivial SKILL.md body.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nashirjamali](https://clawhub.ai/user/nashirjamali)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill as a repeatable checklist for validating that a Skillweave or ClawHub client can publish a skill bundle and that the published artifact contains expected files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad or mishandled ClawHub token could allow unintended publishing activity.

Mitigation: Use a scoped token with only the publish permissions needed for the target namespace or slug.

Risk: Publishing the wrong files or absolute local paths could expose sensitive local details in the uploaded archive.

Mitigation: Review the file list before publishing, include only expected relative paths, and avoid sensitive files.

Risk: Publishing to the wrong slug or version could overwrite or create an unintended release target.

Mitigation: Confirm the slug and semantic version before invoking publishSkill and verify the published listing afterward.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nashirjamali/skills/skillweave-sdk-publish-smoke-test)
- [Publisher profile](https://clawhub.ai/user/nashirjamali)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with checklist steps and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no hidden code or persistence found in server security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
