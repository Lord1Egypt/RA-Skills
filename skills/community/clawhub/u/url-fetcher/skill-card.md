## Description:

Fetches HTML or text from public HTTP/HTTPS URLs, previews or saves the content, and can convert fetched HTML to basic Markdown using only the Python standard library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johstracke](https://clawhub.ai/user/johstracke)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to fetch, preview, and optionally save public web pages as HTML, text, or basic Markdown for content aggregation, research collection, and simple scraping workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says the skill's internal-URL safety checks are too weak for the security claims it makes.

Mitigation: Use it only for trusted public URLs and avoid running it where cloud metadata endpoints or internal HTTP services are reachable.

Risk: The server security guidance warns not to rely on the current file-write checks to protect important files from overwrite.

Mitigation: Save output only to a dedicated scratch directory and review requested output paths before execution.

Risk: The artifact documents no built-in rate limiting for repeated fetches.

Mitigation: Add delays for batch fetching and respect site crawling policies before collecting multiple pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johstracke/skills/url-fetcher)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [CLI output plus fetched HTML, text, or basic Markdown content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python stdlib urllib, no external dependencies or API keys, and a 10-second fetch timeout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
