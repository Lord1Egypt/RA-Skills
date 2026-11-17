## Description:

SwipeNode Web Extractor helps agents fetch webpages and extract structured JSON or readable text without rendering the page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirtoby99](https://clawhub.ai/user/sirtoby99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill when an agent needs to read a webpage, summarize article content, check web pages, or extract structured data from a URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to websites and may be used with sensitive or restricted URLs.

Mitigation: Use only user-approved URLs, avoid credentials and private data in targets, and respect site terms and legal constraints.

Risk: The skill supports browser/TLS impersonation behavior that can bypass some site protections.

Mitigation: Use impersonation only with explicit intent and for legitimate access patterns that comply with site rules and applicable law.

Risk: The packaged skill relies on an externally installed CLI that is not fully auditable from the package alone.

Mitigation: Install only when the upstream project is trusted, avoid elevated privileges, and review the installed release before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sirtoby99/skills/swipenode)
- [ClawHub publisher profile](https://clawhub.ai/user/sirtoby99)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may invoke an externally installed CLI that makes outbound web requests to user-specified URLs.]

## Skill Version(s):

1.6.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
