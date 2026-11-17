## Description:

Use WebTorrent to implement streaming BitTorrent client functionality in Node.js and the browser, including torrent downloading, seeding, magnet links, streaming media playback, and peer-to-peer transfer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement WebTorrent-based download, seeding, magnet link, browser P2P, and streaming media workflows in Node.js or browser applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Torrent and P2P activity can download or seed content and may expose network identifiers to peers or trackers.

Mitigation: Use the skill only when torrent behavior is intentional, require clear user consent before seeding, and confirm that selected content is authorized to share.

Risk: Dependency installation through npm, global CLI installs, or unversioned CDN imports can introduce supply-chain risk.

Mitigation: Pin and review npm dependencies, avoid global installs where possible, and prefer versioned package or CDN references.

Risk: Unbounded downloads or broad file selection can consume storage, bandwidth, or memory.

Mitigation: Set explicit download paths, file-selection rules, storage strategy, and upload/download limits before running torrent workflows.

## Reference(s):

- [WebTorrent Complete API Reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API usage patterns, environment notes, and torrent client configuration options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
