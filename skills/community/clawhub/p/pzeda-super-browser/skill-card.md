## Description:

Browser automation through the published `@pzeda/super-browser` package and its `super-browser` CLI against a real local Chrome session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zipper-319](https://clawhub.ai/user/zipper-319)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to open pages, inspect rendered browser state, click through site flows, upload files, capture screenshots, inspect network requests, and reuse a local Chrome session when browser-backed decisions are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the user to run an unpinned third-party npm package or npx command.

Mitigation: Prefer a reviewed, pinned package version before installation or execution.

Risk: The skill can operate against a real logged-in Chrome session and sensitive browser activity.

Mitigation: Use a dedicated Chrome profile where possible, avoid sensitive sites unless required, and do not capture or share network traffic or screenshots containing secrets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zipper-319/skills/pzeda-super-browser)
- [Publisher Profile](https://clawhub.ai/user/zipper-319)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser page identifiers, screenshots, page-state summaries, network-request summaries, and decision workflow guidance through the referenced CLI.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
