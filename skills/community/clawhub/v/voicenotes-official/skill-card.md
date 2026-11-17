## Description:

This official skill from the Voicenotes team gives OpenClaw access to APIs for semantic note search, full transcript retrieval, tag or date filtering, and text note creation through natural conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gthu-vn](https://clawhub.ai/user/gthu-vn)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an OpenClaw agent search, retrieve, filter, and create notes in their own Voicenotes account through authenticated API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose note contents and search terms to Voicenotes through authenticated API requests.

Mitigation: Use it only with Voicenotes accounts trusted for the relevant note contents, and avoid sending secrets or regulated information unless that is appropriate for the account.

Risk: The skill can create notes or retrieve transcripts in the user's Voicenotes account.

Mitigation: Review requested account actions before execution and keep the API key scoped to the intended Voicenotes account.

Risk: Unsafe interpolation of search queries, recording IDs, or JSON fields could alter generated shell commands.

Mitigation: URL-encode search queries, validate recording IDs against the documented alphanumeric pattern, and JSON-encode request bodies instead of concatenating raw user input.

## Reference(s):

- [Voicenotes homepage](https://voicenotes.com)
- [Voicenotes OpenClaw integration setup](https://voicenotes.com/app?open-claw=true#settings)
- [Voicenotes Official ClawHub listing](https://clawhub.ai/gthu-vn/skills/voicenotes-official)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown with curl commands, YAML configuration, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VOICENOTES_API_KEY and curl; API calls operate on the user's authenticated Voicenotes account.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
