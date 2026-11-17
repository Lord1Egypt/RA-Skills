## Description:

Updates OpenClaw from source with a configurable project path and branch, including fetching upstream changes, merging, building, installing, and restarting the service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hacksing](https://clawhub.ai/user/hacksing)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to update an existing OpenClaw source checkout after reviewing local Git state, selecting a branch, backing up configuration, and confirming update actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The updater can fetch, build, globally install, and restart code from an unverified existing Git remote.

Mitigation: Run it only in a trusted OpenClaw checkout after independently verifying the upstream remote URL.

Risk: The security guidance reports that dry-run behavior should not be relied on until the dry-run bug is fixed.

Mitigation: Review planned commands manually and avoid treating dry-run output as a complete safety control until that issue is resolved.

Risk: Global install, service restart, and force-push guidance can affect the local system or source history.

Mitigation: Back up configuration, commit or stash local changes, avoid sudo or global install unless necessary, and use force push only when explicitly intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hacksing/skills/safe-update)
- [Publisher profile](https://clawhub.ai/user/hacksing)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and command-line options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose update commands that fetch, build, globally install, and restart OpenClaw after user confirmation.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
