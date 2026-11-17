## Description:

Fetch web pages via TinyFish Fetch API and get clean markdown, HTML, or screenshots back \u2014 handles JS rendering and proxying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bunsdev](https://clawhub.ai/user/bunsdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch one or more web pages through TinyFish and receive rendered markdown, HTML, or screenshot data when ordinary page retrieval is unreliable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs and rendered page content are sent to TinyFish.

Mitigation: Use only approved public or non-sensitive URLs, and avoid internal, private, regulated, or token-bearing URLs unless the organization approves that data flow.

Risk: The helper can expose the TinyFish API key in local curl process arguments.

Mitigation: Prefer passing the API key through a protected curl config or file descriptor, and avoid logging commands or process arguments that include the key.

## Reference(s):

- [TinyFish Fetch API documentation](https://docs.tinyfish.ai/fetch-api)
- [TinyFish API keys](https://agent.tinyfish.ai/api-keys)
- [ClawHub skill page](https://clawhub.ai/bunsdev/skills/tinyfish-fetch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline bash commands; API responses are JSON containing rendered markdown, HTML, or base64 PNG screenshot data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TINYFISH_API_KEY and may accept multiple URLs plus optional format and country parameters.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
