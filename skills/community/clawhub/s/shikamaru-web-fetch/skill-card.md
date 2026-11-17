## Description:

Fetch a known URL and return the page as markdown, plain text, raw HTML, or a downloaded image file using the local fetch.js helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shikamaru-cc](https://clawhub.ai/user/shikamaru-cc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they already have a target URL and need the agent to retrieve, inspect, quote, summarize, convert, or save that page or asset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact arbitrary network locations.

Mitigation: Use it only for URLs the user intentionally wants fetched and avoid internal or private network addresses.

Risk: Fetched content may be untrusted.

Mitigation: Review retrieved content before quoting, summarizing, or using it to drive further agent actions.

Risk: Image downloads can overwrite writable files at the selected output path.

Mitigation: Save images only to a safe temporary or download directory where overwrites are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shikamaru-cc/skills/shikamaru-web-fetch)
- [Publisher Profile](https://clawhub.ai/user/shikamaru-cc)

## Skill Output:

**Output Type(s):** [Markdown, Text, Code, Files]

**Output Format:** [Markdown, plain text, raw HTML, or saved image file path in a web_fetch block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses over 5 MB are rejected; timeout can be set up to 120 seconds.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
