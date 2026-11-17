## Description:

Accesses websites with advanced bot protection to fetch HTML, screenshots, PDFs, or multiple pages in parallel using isolated browser contexts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xthezealot](https://clawhub.ai/user/xthezealot)

### License/Terms of Use:

MIT

## Use Case:

Developers and authorized operators use this skill to retrieve page HTML, screenshots, PDFs, or batched page content from websites that present bot-detection challenges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stealth browsing can be used to bypass bot protections on sites where automated access is not authorized.

Mitigation: Use only when there is an explicitly authorized need, and do not use it against sites where automated access or bot-defense bypass is not permitted.

Risk: Server security evidence reports unsafe execution, network, and install behavior that needs review before use.

Mitigation: Run only in a disposable, isolated environment with tight outbound network controls, and review or fix the package before normal use.

Risk: Fetched page content, screenshots, and PDFs can contain sensitive third-party or user data.

Mitigation: Limit targets to authorized, non-sensitive pages where possible and handle generated files as sensitive until reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xthezealot/skills/xthezealot-stealth-browser)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)
- [Package Metadata](artifact/package.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown or plain text responses with fetched HTML previews, JSON summaries for parallel fetches, and file paths for generated screenshots or PDFs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Open responses may be truncated; screenshot and PDF actions write generated files under /tmp.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
