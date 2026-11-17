## Description:

Vocab Voyage MCP provides vocabulary practice, definitions, quizzes, course word lists, study plan previews, progress-aware review, and interactive mini-games for standardized test preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaideepdhanoa](https://clawhub.ai/user/jaideepdhanoa)

### License/Terms of Use:

MIT

## Use Case:

Students, tutors, parents, and education-focused agents use this skill to look up vocabulary, generate test-specific quizzes, preview study plans, and run vocabulary practice for ISEE, SSAT, SAT, PSAT, GRE, GMAT, LSAT, and academic vocabulary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted service may store account-linked study activity, answers, XP, mastery state, and referral-linked usage records.

Mitigation: Use anonymous access for public practice when personalization is not needed, and provide a personal token only when account-linked progress features are desired.

Risk: One documented install path runs an unpinned third-party package through npx.

Mitigation: Prefer the OpenClaw remote install path, or pin and review the mcp-remote package before using the npx-based setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaideepdhanoa/skills/vocab-voyage-mcp-v1-1-1)
- [Publisher profile](https://clawhub.ai/user/jaideepdhanoa)
- [Vocab Voyage MCP tools](https://vocab.voyage/mcp/tools)
- [Vocab Voyage developer docs](https://vocab.voyage/developers)
- [Authentication and scopes](https://vocab.voyage/developers/auth)
- [OpenAPI schema](https://vocab.voyage/openapi.json)
- [MCP server card](https://vocab.voyage/.well-known/mcp/server-card.json)
- [OpenClaw quickstart](docs/openclaw-quickstart.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or structured MCP tool responses with optional interactive widgets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use anonymous access for public vocabulary tools; personalized progress features require an optional bearer token.]

## Skill Version(s):

1.1.1 (source: server evidence release.version, target metadata, artifact CHANGELOG, and artifact manifests)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
