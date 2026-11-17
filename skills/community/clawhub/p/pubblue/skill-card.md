## Description:

Publish and visualize output via the pubblue CLI, with live P2P browser sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmanatee](https://clawhub.ai/user/xmanatee)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to create, update, list, and delete pub.blue pages for sharing HTML, Markdown, or text output, and to manage live browser canvas/chat sessions through the pubblue CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable npm execution or unreviewed CLI updates could change runtime behavior.

Mitigation: Use a pinned, reviewed pubblue CLI version before installing or running commands.

Risk: API-key configuration and persistent daemon behavior can expose credentials or leave live sessions active.

Mitigation: Avoid placing real API keys in command history or shared transcripts, use a restricted config directory when possible, and stop the daemon when live sessions are no longer needed.

Risk: Publishing and deletion commands can accidentally expose sensitive content or remove pubs unexpectedly.

Mitigation: Confirm public/private settings and delete behavior before use, and avoid publishing sensitive content accidentally.

## Reference(s):

- [ClawHub Pubblue skill page](https://clawhub.ai/xmanatee/skills/pubblue)
- [pub.blue dashboard](https://pub.blue/dashboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce shareable pub.blue pages and live browser canvas/chat session content; pubs are private by default.]

## Skill Version(s):

5.1.2 (source: frontmatter, claw.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
