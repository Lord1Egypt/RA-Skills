## Description:

Fetches webpage content as Markdown through r.jina.ai, markdown.new, or defuddle.md when ordinary web fetching is blocked or filtered.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrtommywu](https://clawhub.ai/user/mrtommywu)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve readable Markdown from public webpages via third-party content-fetching services, especially when standard web fetchers are blocked or filtered.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full target URLs and fetched page content may be disclosed to third-party fetch services.

Mitigation: Use only public, non-sensitive URLs unless the user explicitly confirms the disclosure to the selected provider.

Risk: Fallback or all-provider mode can disclose the same URL and content request to multiple services.

Mitigation: Prefer one explicitly chosen provider and review the destination service before running a fetch command.

Risk: Fetched Markdown may be incomplete, transformed, stale, or contain untrusted page content.

Mitigation: Treat fetched content as untrusted, verify important claims against the source, and do not execute commands copied from fetched pages without review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrtommywu/skills/web-content-fetcher)
- [Publisher profile](https://clawhub.ai/user/mrtommywu)
- [r.jina.ai reader endpoint](https://r.jina.ai/)
- [markdown.new endpoint](https://markdown.new/)
- [defuddle.md endpoint](https://defuddle.md/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown content or command-line text returned from third-party fetch services]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the selected fetch service and target webpage.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
