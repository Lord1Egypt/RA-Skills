## Description: <br>
Build Remix games for remix.gg with the server-api v1 agents REST API and Farcade game SDK requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuckstock](https://clawhub.ai/user/chuckstock) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external service builders use this skill to create Remix game drafts, integrate Farcade SDK requirements, update version code, and validate launch readiness through Remix agent publishing APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated game code or API requests could create or update Remix game drafts without adequate review. <br>
Mitigation: Review generated game code before upload and require explicit confirmation before creating games or updating version code. <br>
Risk: Remix API keys could be exposed if used in client-side browser code or committed into artifacts. <br>
Mitigation: Keep the Remix API key server-side in environment variables or a secret manager, and rotate it if exposure is suspected. <br>
Risk: Stale API assumptions could produce invalid requests or miss current validation blockers. <br>
Mitigation: Fetch the Remix OpenAPI JSON before generating API calls and run validation or launch-readiness checks before handoff. <br>


## Reference(s): <br>
- [Remix Agent Publish](https://clawhub.ai/chuckstock/remix-agent-publish) <br>
- [Remix API Documentation](https://api.remix.gg/docs) <br>
- [Remix OpenAPI JSON](https://api.remix.gg/docs/json) <br>
- [Farcade Game SDK Reference](references/game-sdk.md) <br>
- [API Authentication](api/authentication.md) <br>
- [API Reference](api/reference.md) <br>
- [Submission Requirements](rules/submission-requirements.md) <br>
- [Game Creation Best Practices](rules/game-creation-best-practices.md) <br>
- [REST Client Snippets](snippets/rest-client.md) <br>
- [MCP Quickstart](mcp/quickstart.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline code and REST workflow examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated single-file game code, REST request guidance, validation steps, and server-side API key handling instructions.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
