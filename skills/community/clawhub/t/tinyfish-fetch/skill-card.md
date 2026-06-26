## Description: <br>
Fetch web pages via the TinyFish Fetch API and return clean markdown, HTML, or screenshots with support for JavaScript rendering and proxy targeting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bunsdev](https://clawhub.ai/user/bunsdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch one or more web pages through TinyFish when they need rendered page content as markdown, HTML, or screenshot output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs and fetched page content are sent to TinyFish. <br>
Mitigation: Use only for URLs whose disclosure to TinyFish is approved; avoid private intranet, localhost, cloud metadata, authenticated links, and URLs containing tokens. <br>
Risk: The skill requires a TinyFish API key. <br>
Mitigation: Store TINYFISH_API_KEY securely and avoid logging, committing, or sharing it. <br>


## Reference(s): <br>
- [TinyFish Fetch API documentation](https://docs.tinyfish.ai/fetch-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, HTML, or base64 PNG screenshot content returned by API calls; examples are shell commands and JSON request and response shapes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TINYFISH_API_KEY; requested URLs and fetched content are processed by TinyFish.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
