## Description:

Use when the user asks to open, preview, inspect, or visually edit an existing SenseNova HTML presentation in the PPT Workbench, using an explicit deck_dir or the latest deck in the current workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers who already have a SenseNova HTML slide deck use this skill to open, preview, inspect, or visually edit it in the PPT Workbench.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reachable users may access sensitive workbench controls and files.

Mitigation: Do not expose this release through LAN access or public forwarding. Loopback binding reduces exposure but does not fix the underlying flaws.

Risk: The agent integrations grant excessive authority, with concerns involving conversation sharing and profile replacement.

Mitigation: Evaluate only in an isolated environment without personal credentials or private conversations; back up decks and profiles, and prefer a release that fixes these issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-ppt-workbench)
- [Gateway Authentication Setup](references/gateway-auth.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Web UI links]

**Output Format:** [Text with a workbench URL and status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an editor URL, startup status, or a reason startup was skipped or failed.]

## Skill Version(s):

2026.10.29 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
