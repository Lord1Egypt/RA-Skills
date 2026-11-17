## Description:

Generate social images and OG cards from professional templates via the SnapOG API. One API call = one pixel-perfect PNG.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beameasy](https://clawhub.ai/user/beameasy)

### License/Terms of Use:


## Use Case:

Developers, marketers, and content teams use this skill to generate OG images, social cards, and marketing visuals from SnapOG templates through authenticated API calls or signed image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image text, template parameters, referenced asset URLs, and generated signed URLs may expose sensitive campaign or personal data to SnapOG or downstream viewers.

Mitigation: Do not use secrets, private URLs, confidential campaign data, or regulated personal data in image parameters or referenced assets.

Risk: The SNAPOG_API_KEY and signed image URLs can function as bearer-style credentials if exposed in code, logs, screenshots, or shared command history.

Mitigation: Keep the API key out of code and logs, store it only in environment variables or approved secret stores, and avoid sharing signed URLs beyond intended audiences.

## Reference(s):

- [SnapOG Skill on ClawHub](https://clawhub.ai/beameasy/skills/snapog)
- [SnapOG Homepage](https://snapog.dev)
- [SnapOG API Base](https://api.snapog.dev)
- [SnapOG API Docs](https://api.snapog.dev/v1/docs)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to produce or embed generated image files and signed image URLs using SnapOG template parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
