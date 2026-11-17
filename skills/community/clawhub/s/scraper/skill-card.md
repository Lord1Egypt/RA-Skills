## Description:

Structured extraction and cleanup for public, user-authorized web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch public, user-authorized web pages, extract readable text, and save cleaned local outputs for downstream summarization, transformation, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL-fetching scripts do not enforce the documented public-only boundary and may be directed at local, private-network, link-local, local-file, or redirected destinations.

Mitigation: Use only personally trusted public URLs until scheme and destination allowlists, private-address blocking, unsafe redirect blocking, and response-size limits are implemented.

Risk: The skill can save extracted page content locally.

Mitigation: Use it only for public or user-authorized content and avoid pages containing credentials, private data, paywalled material, or access-controlled content.

## Reference(s):

- [Scraper Safety](artifact/references/safety.md)
- [ClawHub Scraper skill page](https://clawhub.ai/agistack/skills/scraper)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands, plain text extraction output, and local text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local-only; fetch and extraction scripts print up to 4000 characters, while saved outputs are written under ~/.openclaw/workspace/memory/scraper/.]

## Skill Version(s):

1.0.0 (source: evidence release, artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
