## Description:

Provides AI tools to generate and deliver creative content including rich Markdown, PDFs, CSVs, AI-generated images, videos, web media, and GitHub repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulgnz](https://clawhub.ai/user/paulgnz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create, package, store, and publish creative job deliverables such as Markdown, PDFs, generated images, generated videos, CSVs, media files, and code repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deliverables can be sent to external services and may become public through IPFS or public GitHub repositories.

Mitigation: Require explicit approval before IPFS uploads or public repository creation, avoid sensitive or proprietary content, and confirm the intended destination before delivery.

Risk: Outbound URL fetching can retrieve untrusted remote media and content.

Mitigation: Isolate URL fetching from internal networks and review source URLs before use.

Risk: Service credentials are required for some publishing and generation paths.

Mitigation: Use narrowly scoped Pinata, Replicate, and GitHub tokens and rotate them according to local credential policy.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, shell commands, guidance]

**Output Format:** [Markdown, JSON tool responses, media URLs, data URIs, IPFS URLs, and public GitHub repository URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create externally hosted deliverables through IPFS, Replicate, Pinata, and GitHub when configured with service credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
