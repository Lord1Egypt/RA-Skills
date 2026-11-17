## Description:

Generate AI YouTube thumbnail images with the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sherrihidalgolt](https://clawhub.ai/user/sherrihidalgolt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate YouTube thumbnail image URLs from text prompts through the Neta AI service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and the Neta token to the remote api.talesofai.com backend.

Mitigation: Verify that api.talesofai.com is the intended service for the token and avoid sending sensitive prompt content.

Risk: Passing real tokens on command lines can expose them through shell history or process inspection.

Mitigation: Use short-lived or least-privilege tokens where possible and avoid preserving commands that contain production tokens.

Risk: Unpinned installs can change the code executed by the agent over time.

Mitigation: Prefer a pinned release or ClawHub-managed install path before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sherrihidalgolt/skills/thumbnail-gen-skill)
- [Neta API access](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API Calls]

**Output Format:** [Plain text image URL printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token passed with --token; supports size selection and an optional reference image UUID.]

## Skill Version(s):

2.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
