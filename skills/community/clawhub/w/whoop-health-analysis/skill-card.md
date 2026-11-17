## Description:

Access Whoop wearable health data (sleep, recovery, strain, HRV, workouts) and generate interactive charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rodrigouroz](https://clawhub.ai/user/rodrigouroz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to authenticate with Whoop, retrieve personal wearable health metrics, analyze sleep, recovery, strain, HRV, workouts, profile, and body-measurement data, and generate interactive health charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read access to sensitive Whoop health, profile, and body-measurement data.

Mitigation: Install and run it only on a private machine, grant access only when the data scope is acceptable, and revoke the Whoop app authorization when access is no longer needed.

Risk: OAuth credentials and tokens are handled locally with weak protections.

Mitigation: Avoid passing secrets in shared shells, restrict local file access, and rotate or revoke credentials if logs, terminals, or generated files may have been exposed.

Risk: Generated HTML reports may expose personal health data and load unpinned third-party JavaScript.

Mitigation: Do not share generated reports without review, and prefer bundled or pinned chart JavaScript before using reports in sensitive environments.

## Reference(s):

- [Whoop API Reference](references/api.md)
- [Health Data Analysis Guide](references/health_analysis.md)
- [Whoop Developer Dashboard](https://developer-dashboard.whoop.com)
- [Whoop Developer API](https://api.prod.whoop.com/developer/v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON API data, and generated HTML chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive HTML reports may open in a browser and contain personal health data.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
