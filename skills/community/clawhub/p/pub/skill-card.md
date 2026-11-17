## Description:

Create adaptive interfaces and real-time experiences via the pub CLI, with live P2P browser sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmanatee](https://clawhub.ai/user/xmanatee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, publish, update, and run live browser-based interfaces through the pub CLI. It supports shareable HTML, Markdown, text, live canvas output, and P2P chat or canvas sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation or updates through remote shell scripts, latest-release downloads, or self-update commands can run code that was not pinned or independently verified.

Mitigation: Prefer a pinned GitHub release with checksum or signature verification, review the release before installation, and avoid pipe-to-bash installation when possible.

Risk: Publishing generated content or live-session output may expose secrets, private files, or unintended internal context.

Mitigation: Use private pubs by default, publish only user-selected content, check for secrets or private data before sharing, and stop the live daemon when finished.

## Reference(s):

- [Pub homepage](https://pub.blue)
- [Pub agent setup](https://pub.blue/agents)
- [Pub latest release](https://github.com/xmanatee/pub/releases/latest)
- [ClawHub skill page](https://clawhub.ai/xmanatee/skills/pub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and HTML, Markdown, or text content for pub publishing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update private-by-default pubs, start live sessions, and write chat or canvas output through the pub CLI.]

## Skill Version(s):

5.2.17 (source: server release metadata, artifact metadata, and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
