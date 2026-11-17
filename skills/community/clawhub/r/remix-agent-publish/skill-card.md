## Description:

Build Remix games for remix.gg with the server-api v1 agents REST API and Farcade game SDK requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuckstock](https://clawhub.ai/user/chuckstock)

### License/Terms of Use:


## Use Case:

Developers and AI-agent operators use this skill to create Remix game drafts, generate or repair Farcade-compatible game code, update draft versions through the Remix agent REST API, and validate launch readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Remix API key can authorize changes to live account resources if exposed or reused carelessly.

Mitigation: Use a scoped or test Remix API key where possible, store it only in server-side secrets or environment variables, and rotate or revoke it from Remix account settings when needed.

Risk: The REST snippet creates game drafts and updates Remix versions, so running it against a real account can change live draft state.

Mitigation: Review generated REST calls before execution, confirm target game and version identifiers, and run validation or launch-readiness checks before relying on the draft.

Risk: Sending Authorization headers to public documentation endpoints can unnecessarily expose credentials in logs or intermediaries.

Mitigation: Fetch public OpenAPI documentation without authorization headers unless the endpoint explicitly requires authenticated access.

## Reference(s):

- [Remix Agent Publish on ClawHub](https://clawhub.ai/chuckstock/skills/remix-agent-publish)
- [Remix OpenAPI JSON](https://api.remix.gg/docs/json)
- [Remix OpenAPI UI](https://api.remix.gg/docs)
- [Remix API Keys](https://remix.gg/api-keys)
- [Farcade Game SDK CDN](https://cdn.jsdelivr.net/npm/@farcade/game-sdk@0.3.0/dist/index.min.js)
- [Farcade Game SDK Reference](artifact/references/game-sdk.md)
- [Submission Requirements](artifact/rules/submission-requirements.md)
- [Game Creation Best Practices](artifact/rules/game-creation-best-practices.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST examples, validation checklists, and code-generation constraints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TypeScript REST snippets and single-file HTML game implementation guidance for Remix/Farcade workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
