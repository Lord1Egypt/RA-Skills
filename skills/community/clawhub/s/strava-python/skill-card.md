## Description: <br>
Query Strava activities, stats, and workout data using Python/stravalib with interactive setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abclark](https://clawhub.ai/user/abclark) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent query their Strava activities, weekly/monthly running and cycling stats, and last workout after an interactive OAuth setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Strava OAuth setup requests broad read access, including private activity and profile data. <br>
Mitigation: Install only if that access is acceptable, review the requested scopes during authorization, and revoke the Strava app authorization when access is no longer needed. <br>
Risk: The setup stores Strava tokens and the client secret in a plaintext local credentials file. <br>
Mitigation: Restrict ~/.strava_credentials.json to the local user account, avoid shared or untrusted machines, and revoke or rotate credentials if the file may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abclark/strava-python) <br>
- [Strava](https://www.strava.com) <br>
- [Strava API app settings](https://www.strava.com/settings/api) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text summaries with setup and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Strava OAuth credentials and the stravalib Python package.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and changelog, released 2026-02-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
