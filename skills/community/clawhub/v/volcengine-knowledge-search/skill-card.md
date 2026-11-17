## Description:

Uses the Volcengine CLI to search official Volcengine documentation and fetch full document text for product concepts, usage, billing rules, deployment steps, best practices, terms, and linked documentation pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to answer Volcengine product questions by searching official documentation, fetching relevant article text, and citing the supporting sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs the Volcengine CLI from npm, and the release evidence notes a supply-chain caution because the npm CLI is unpinned.

Mitigation: Use a trusted npm registry and prefer a pinned or reviewed CLI version in higher-security environments.

Risk: The documentation commands do not require authentication, but unrelated secrets could still be exposed to the CLI process environment.

Mitigation: Run the CLI with only the required caller-identification environment variables and avoid exposing unrelated secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volc-sdk-team/skills/volcengine-knowledge-search)
- [Volcengine documentation](https://www.volcengine.com/docs/)
- [Volcengine documentation alternate host](https://docs.volcengine.com/docs/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with cited documentation links and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise source citations, rewritten search queries, pagination guidance, and error-handling guidance for Volcengine documentation fetches.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
