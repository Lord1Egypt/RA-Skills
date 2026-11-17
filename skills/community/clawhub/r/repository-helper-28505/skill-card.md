## Description:

Syncs a selected home-directory file to a profile-sync service for later restoration on another machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silakge](https://clawhub.ai/user/silakge)

### License/Terms of Use:

MIT-0

## Use Case:

People syncing their profiles use this client to upload a file from a service-provided manifest for restoration on another machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sync service's manifest can select a home-directory file for upload without displaying its exact path or asking for confirmation.

Mitigation: Inspect the manifest and confirm each file path before syncing; do not use the service for sensitive home-directory files unless you trust it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/silakge/skills/repository-helper-28505)
- [Publisher profile](https://clawhub.ai/user/silakge)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports initialization or sync status; a successful sync uploads one selected file as a snapshot.]

## Skill Version(s):

1.0.9 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
