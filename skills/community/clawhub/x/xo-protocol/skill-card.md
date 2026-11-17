## Description:

Dating intelligence API for identity verification, compatibility scoring, reputation, and social signals via XO Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pbjhsu](https://clawhub.ai/user/pbjhsu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent builders use this skill to connect agents or dating applications to XO Protocol for user-authorized identity, compatibility, reputation, profile, and public-post signals. It supports trust badges, social-context workflows, ranking, and scam-review assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An AI client can access XO account-linked trust, reputation, profile, and public-post data through a user's XO token.

Mitigation: Install only for clients that should receive this data, disclose the data access to end users, and request only the OAuth scopes needed for the task.

Risk: XO_API_KEY and XO_ACCESS_TOKEN can expose authorized API access if copied into shared configuration or logs.

Mitigation: Keep credentials out of shared config, source control, and transcripts; rotate tokens if they are exposed.

Risk: OAuth example code may be incomplete for production token handling and state validation.

Mitigation: Harden production integrations with token isolation, state validation, PKCE where appropriate, and normal application security review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pbjhsu/skills/xo-protocol)
- [XO Protocol landing page](https://xoxo.space/en/protocol)
- [XO Protocol API docs](https://protocol.xoxo.space/protocol/docs)
- [OpenAPI specification](https://github.com/xo-protocol/xo-protocol/blob/main/openapi.yaml)
- [XO Protocol SDK](https://github.com/xo-protocol/xo-protocol/tree/main/sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, configuration snippets, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP/API results require XO_API_KEY and XO_ACCESS_TOKEN and depend on the user's approved OAuth scopes.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata and SKILL.md frontmatter; SDK package and OpenAPI list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
