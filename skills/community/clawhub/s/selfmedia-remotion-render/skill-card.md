## Description:

Render an existing Remotion composition from a user-selected project using that project's installed toolchain, then verify the output against the requested render settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and video creators use this skill to render an existing Remotion composition with the selected project's installed toolchain and check the resulting video against requested settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering executes code from the selected local project.

Mitigation: Use trusted projects and check and lock their resolved dependency versions before rendering.

Risk: A render may not match the requested settings or may be incomplete.

Mitigation: Use a fresh output path and inspect the finished video against the requested settings.

## Reference(s):

- [Remotion render guide](https://www.remotion.dev/docs/render)
- [Remotion CLI render reference](https://convert.remotion.dev/docs/cli/render)

## Skill Output:

**Output Type(s):** [Video files, Guidance, Shell commands]

**Output Format:** [Rendered video file with concise text verification guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the requested composition settings and user-selected output path.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
