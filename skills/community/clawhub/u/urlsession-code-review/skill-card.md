## Description:

Reviews iOS and macOS URLSession networking code for async/await usage, request construction, error handling, caching, and background-session issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Swift networking code that uses URLSession, URLRequest, URLCache, HTTPURLResponse, or URLError. It helps produce prioritized Markdown review findings with file and line citations, concrete issues, and fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to propose networking code changes that affect request construction, caching, downloads, or secrets handling.

Mitigation: Review proposed changes before applying them, especially changes touching credentials, URL construction, background sessions, and file transfers.

## Reference(s):

- [URLSession Async/Await Reference](references/async-networking.md)
- [URLRequest Building Reference](references/request-building.md)
- [URLSession Error Handling Reference](references/error-handling.md)
- [URLSession Caching and Configuration Reference](references/caching.md)
- [Apple Developer Documentation: URLSessionDataDelegate caching](https://developer.apple.com/documentation/foundation/urlsessiondatadelegate/urlsession(_:datatask:willcacheresponse:completionhandler:))

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Guidance]

**Output Format:** [Markdown review findings with inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are gated by scope checks and should cite files and lines before reporting critical issues.]

## Skill Version(s):

1.2.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
