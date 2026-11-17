## Description:

Turn a user-provided PNG or JPEG line-art illustration into a hand-drawn scribe animation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boring-stuff-club](https://clawhub.ai/user/boring-stuff-club)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, monitor, download, unlock, or delete prompt-directed scribe animations from PNG or JPEG line-art images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User artwork is uploaded to an external service and may be retained according to the service's current policy.

Mitigation: Call the service information tool before creation, disclose the current retention, terms, and pricing, and obtain explicit user confirmation before uploading.

Risk: A private management link or capability token can grant access to a generated animation.

Mitigation: Treat management links, animation IDs, and capability tokens as sensitive and avoid exposing them in ordinary chat text, logs, filenames, or unrelated tools.

Risk: Uploaded artwork may be subject to rights or licensing restrictions.

Mitigation: Ask the user to confirm they have the rights needed to process the artwork before creating an animation.

## Reference(s):

- [The Scribble Thing MCP endpoint](https://scribble.boringstuff.club/mcp)
- [The Scribble Thing REST fallback guide](https://scribble.boringstuff.club/docs/agent-api)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Files]

**Output Format:** [Markdown with links to generated animation previews, management pages, or short-lived downloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MP4 scribe animations through a disclosed external service; clean downloads may require user-managed unlock or purchase.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
