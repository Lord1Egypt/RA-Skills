## Description:

Turn Markdown content into a shareable md.page web page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maypaz](https://clawhub.ai/user/maypaz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to publish generated or existing Markdown as a temporary md.page URL for sharing reports, notes, documentation, or other Markdown content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown that contains private or sensitive information could be uploaded unintentionally.

Mitigation: Confirm the user intends to publish the content, avoid private or sensitive files, and scan existing files for secrets before upload.

Risk: The documented inline Python interpolation pattern can create avoidable local code-execution risk.

Mitigation: Use a stdin- or file-based JSON encoding workflow instead of interpolating untrusted Markdown into inline Python code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maypaz/skills/publish-to-mdpage)
- [md.page](https://md.page)
- [md.page publish API](https://md.page/api/publish)

## Skill Output:

**Output Type(s):** [text, shell commands, API calls, guidance]

**Output Format:** [Text response with a published URL and optional error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishes Markdown up to 500KB; artifact documentation says returned pages expire in 24 hours.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
