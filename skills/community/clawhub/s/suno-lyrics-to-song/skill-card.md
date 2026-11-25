## Description:

Helps users shape existing lyrics into a structured Suno song with custom lyrics and clear musical direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators use the skill to preserve or refine their lyrics, organize song sections, and prepare a Suno song with a clear style, arrangement, and vocal direction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports broad shared permissions for the connected service.

Mitigation: Review the authorization scope before connecting and proceed only if the shared access is acceptable for the intended use.

Risk: The skill makes an installation registration that includes coarse environment and installation information.

Mitigation: Review the registration details and Beatra privacy information before use; registration is described as best effort and non-blocking.

Risk: Uninstalling the last Beatra skill on a device can revoke its shared device credential and remove shared connection state.

Mitigation: Use the bundled uninstall workflow and review its decision output so shared connection state is removed only when no other Beatra skill remains.

Risk: The security scan is partial, with unresolved references and an icon outside analyzer coverage.

Mitigation: Treat the suspicious verdict as a reason for added review, while recognizing that the evidence does not establish malicious intent.

## Reference(s):

- [Lyrics intake and modes](artifact/references/lyrics-intake-and-modes.md)
- [Song direction and request](artifact/references/song-direction-and-request.md)
- [Workflow](artifact/references/workflow.md)
- [Updates and security](artifact/references/updates-and-security.md)
- [Uninstall and disconnect](artifact/references/uninstall-and-disconnect.md)
- [Beatra service](https://beatra.ai)
- [Beatra MCP service](https://mcp.beatra.ai/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Audio]

**Output Format:** [Structured lyrics and song-production direction in Markdown, with generated audio when requested and available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lyrics may be preserved exactly or refined with the user's permission; paid generation requires confirmation.]

## Skill Version(s):

0.3.4 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
