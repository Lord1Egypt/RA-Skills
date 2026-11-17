## Description:

Manage Usenet downloads with SABnzbd, including queue, NZB, speed, history, category, script, and status operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmagar](https://clawhub.ai/user/jmagar)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage a SABnzbd instance from an agent workflow, including viewing queue and history state, adding NZB downloads, changing speed limits, and controlling jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted NZB URL can execute local Python code through the helper script.

Mitigation: Use only trusted NZB URLs, review add commands before execution, and avoid passing untrusted input to the helper script.

Risk: The helper script supports destructive SABnzbd actions such as purge, deleting files, deleting history, and clearing warnings without confirmation.

Mitigation: Require explicit user confirmation before purge, delete with files, delete-history, or warning-clear operations.

Risk: The SABnzbd API key grants control over the configured SABnzbd instance.

Mitigation: Store the API key with owner-only permissions and prefer HTTPS for non-local SABnzbd URLs.

## Reference(s):

- [SABnzbd Skill README](README.md)
- [ClawHub skill page](https://clawhub.ai/jmagar/skills/sabnzbd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and SABnzbd JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SABnzbd URL and API key configuration; command outputs depend on the connected SABnzbd instance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
