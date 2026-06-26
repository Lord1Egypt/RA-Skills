## Description: <br>
Read current values from Grafana dashboards by dashboard and panel name without writing PromQL, SQL, or datasource queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DarkStarDS9](https://clawhub.ai/user/DarkStarDS9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agents use this skill to list Grafana dashboards and panels, then retrieve current or recent metric values from existing panels using read-only Grafana access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Grafana dashboard metrics returned by the skill may contain sensitive operational data. <br>
Mitigation: Install only against trusted Grafana instances and restrict the configured account to dashboards the agent is allowed to read. <br>
Risk: Overprivileged Grafana credentials could expose more dashboard and panel data than intended. <br>
Mitigation: Use a least-privileged Viewer or read-only service account, not admin credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DarkStarDS9/rpe-grafana) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Text tool responses containing compact JSON arrays, with Markdown setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Grafana URL and credentials; query calls use dashboard UID, panel ID, and optional time range.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
