## Description:

Make HTTP requests with custom headers, retries, and graceful error handling using only Node.js built-in modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephen-standridge](https://clawhub.ai/user/stephen-standridge)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to call APIs, fetch URLs, send webhooks, or make HTTP requests without adding external dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad user-directed HTTP requests, including requests with sensitive headers or bodies.

Mitigation: Review request destinations before execution and send Authorization headers or sensitive bodies only to trusted APIs.

Risk: Examples, logs, or generated requests could expose real credentials if secrets are copied into them.

Mitigation: Use placeholders in examples and avoid placing real secrets in logs or shared request snippets.

## Reference(s):


## Skill Output:

**Output Type(s):** [code, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples and structured response objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces inspectable HTTP response objects with status, headers, body, ok, and error fields.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
