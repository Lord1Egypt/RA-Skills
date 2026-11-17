## Description:

Check and control a Wyze robot vacuum: status including battery and cleaning state, start, pause, and send to dock through the unofficial Wyze API via wyze-node.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noelportugal](https://clawhub.ai/user/noelportugal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check Wyze robot vacuum status and issue clear, user-requested controls such as start, pause, or dock for a named vacuum.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Wyze API credentials and cached login tokens.

Mitigation: Store credentials in the configured secret environment file, restrict access to token storage, and review the npm dependency before installation.

Risk: State-changing commands can move a physical vacuum in the user's home.

Mitigation: Only run start, pause, or dock after a clear user request, and act on the named vacuum rather than guessing.

Risk: The skill relies on an unofficial Wyze API client and endpoints that may change.

Mitigation: Prefer a pinned dependency or lockfile and confirm behavior after wyze-node or Wyze API changes.

## Reference(s):

- [Wyze Vacuum on ClawHub](https://clawhub.ai/noelportugal/skills/wyze-vacuum)
- [wyze-node GitHub repository](https://github.com/noelportugal/wyze-node)
- [wyze-node npm package](https://www.npmjs.com/package/wyze-node)
- [Wyze API Key Console](https://developer-api-console.wyze.com/#/apikey/view)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue API-backed status queries or state-changing vacuum commands through the bundled CLI when the user explicitly requests them.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
