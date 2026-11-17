## Description:

Helps agents manage PTBrowser Chromium profiles, groups, proxies, extensions, and archived environments through a signed-in local Windows client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qique](https://clawhub.ai/user/qique)

### License/Terms of Use:

MIT-0

## Use Case:

PTBrowser users and developers use this skill to inspect and manage local browser environments, profiles, groups, proxies, extensions, and archived items with user approval for changes. It does not automate third-party websites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profile changes, archiving, restoration, or deletion may affect the wrong environment.

Mitigation: Read current IDs and state, show the intended change, obtain user approval, and verify the result afterward.

Risk: The separately downloaded runtime package could be untrusted or mismatched.

Mitigation: Download from the publisher's official source and verify its SHA-256 before installation or upgrade.

Risk: Local session files or tokens could expose account access.

Mitigation: Keep session and token files local; do not share their contents with the agent or others.

## Reference(s):

- [PTBrowser setup and local MCP connection](references/setup.md)
- [PTBrowser product website](https://ptbrowser.qique.cn/)
- [Official runtime download and checksum snapshot](distribution/official-downloads.json)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Text]

**Output Format:** [Markdown with tool results and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a signed-in Windows client and separately installed local MCP runtime; state-changing actions require user confirmation.]

## Skill Version(s):

0.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
