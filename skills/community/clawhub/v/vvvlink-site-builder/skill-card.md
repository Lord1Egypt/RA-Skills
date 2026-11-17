## Description:

Builds and publishes HTML websites on vvvlink.com by uploading site files to the VVVLink API and publishing unique subdomain URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vladlat](https://clawhub.ai/user/vladlat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, redesign, upload, and publish static websites, landing pages, portfolios, and business pages to public vvvlink.com URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a VVVLink account and store an API key under ~/.vvvlink.

Mitigation: Install only where local credential storage is acceptable, keep the config file private, and avoid sharing logs or files that may expose credentials.

Risk: The skill publishes generated content to a public vvvlink.com URL without a separate confirmation step.

Mitigation: Use it only for content intended to be public, and remove confidential business or personal details before publishing.

Risk: Cleanup actions can delete published or draft sites.

Mitigation: Confirm the exact target site or site ID before allowing deletion.

## Reference(s):

- [VVVLink Site Builder on ClawHub](https://clawhub.ai/vladlat/skills/vvvlink-site-builder)
- [VVVLink API Reference](references/api-reference.md)
- [Website Development Rules](references/website-development-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status updates with HTML, CSS, JavaScript, shell commands, and published site URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local site files, store VVVLink credentials, call the VVVLink API, and publish content to public vvvlink.com URLs.]

## Skill Version(s):

1.8.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
