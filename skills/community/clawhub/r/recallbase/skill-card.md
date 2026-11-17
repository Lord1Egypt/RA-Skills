## Description:

Recover context from local AI conversation history with RecallBase for same-day work summaries, session resumption, and tracing past decisions to their source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darinrowe](https://clawhub.ai/user/darinrowe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other AI tool users use this skill to retrieve the smallest useful slice of local AI conversation history, then synthesize grounded daily recaps, session-continuation context, or explanations of earlier decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search local AI conversation history, which may include sensitive prior work context.

Mitigation: Install and use it only when local-history retrieval is acceptable, use the narrowest query that answers the request, and summarize relevant evidence instead of reproducing full transcripts.

Risk: If the local rb CLI is missing, installing it globally changes the user's local toolchain.

Mitigation: Verify the npm package and publisher before authorizing a global install.

## Reference(s):

- [RecallBase skill release](https://clawhub.ai/darinrowe/skills/recallbase)
- [Server-resolved GitHub provenance](https://github.com/DarinRowe/RecallBase/tree/main/skills/recallbase)
- [Local MCP](references/mcp.md)
- [Result reference](references/results.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Natural-language answer with concise references and optional inline shell commands or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Material claims should be grounded in retrieved local history, with coverage gaps stated explicitly.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
