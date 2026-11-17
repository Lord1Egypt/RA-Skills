## Description:

Build and publish a Quartz-hosted Korean web-novel serial (draft→cover→webp→episode md→lint→publish). Uses Nano Banana Pro + ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeong-wooseok](https://clawhub.ai/user/jeong-wooseok)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to plan, draft, lint, convert cover images, and publish Korean web-novel episodes into a Quartz-hosted serial site after human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File-writing scripts can write outside the intended draft or Quartz folders if crafted path or filename values are supplied.

Mitigation: Use conservative series and slug values, validate filenames before execution, enforce containment under the configured draft and Quartz roots, and define an explicit overwrite policy before publishing.

Risk: The release security verdict is suspicious because filesystem write boundaries need review.

Mitigation: Install only from a trusted publisher and review the file-writing behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeong-wooseok/skills/webnovel-serial-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python command examples, plus generated Markdown files and WebP assets when scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WEBNOVEL_QUARTZ_ROOT for the Quartz publish target and optionally WEBNOVEL_DRAFT_ROOT and NANO_BANANA_KEY.]

## Skill Version(s):

0.1.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
