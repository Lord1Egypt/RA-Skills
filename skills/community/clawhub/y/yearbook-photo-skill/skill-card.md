## Description:

Generates AI yearbook photo images from text prompts through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate yearbook-style portrait image URLs from text prompts, with optional size and reference-image parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens may be exposed if passed directly on the command line or stored carelessly.

Mitigation: Use secret management or environment variables, avoid shell-history exposure, and rotate any token that may have been disclosed.

Risk: Prompts and reference image IDs are sent to the Neta/talesofai service for image generation.

Mitigation: Submit only prompts and reference image identifiers that are acceptable to share with that external service.

Risk: The release evidence flags broad Bash scope and unpinned installation as review-worthy.

Mitigation: Review the artifact before installation, prefer a pinned or verified install path, and execute it only in an appropriate environment.

## Reference(s):

- [Neta API token and free trial](https://www.neta.art/open/)
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/yearbook-photo-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text image URL with Markdown usage guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and may use optional size and reference-image UUID parameters.]

## Skill Version(s):

1.6.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
