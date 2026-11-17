## Description:

Get a PDF link from Sci-Hub for a DOI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aukaukauk](https://clawhub.ai/user/aukaukauk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to resolve a DOI through Sci-Hub mirrors and return a direct PDF URL when available, or a concise status when no PDF is found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Sci-Hub mirrors and third-party PDF hosts using DOI queries, which may expose requested DOI information and may be legally or institutionally restricted.

Mitigation: Install only where this access is approved, and run it in a network-restricted sandbox that blocks localhost, private networks, link-local addresses, and metadata services.

Risk: Custom SCIHUB_MIRRORS values can direct requests to untrusted hosts.

Mitigation: Use default mirrors or only organization-approved mirror URLs.

Risk: The script automates challenge solving.

Mitigation: Review before installation and avoid use where automated challenge solving violates policy or site terms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aukaukauk/skills/scihub-paper-downloader)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text URL or status line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a direct PDF URL, NOT_FOUND with optional OA_LINK, MIRROR_ERROR, or INVALID_INPUT.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
