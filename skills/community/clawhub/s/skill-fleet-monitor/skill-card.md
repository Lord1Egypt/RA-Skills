## Description: <br>
Scans installed skills for version drift, delisted listings, and related fleet health signals, then reports items that need review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ordo-tech](https://clawhub.ai/user/ordo-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit installed ClawHub/OpenClaw skills after installation, on a schedule, or after a security advisory. It helps identify outdated or delisted skills and, in the fuller workflow, publisher standing, advisory, pattern, and permission concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads installed skill manifests and reports skill names, versions, authors, and risk notes that may reveal local inventory. <br>
Mitigation: Run it only where that inventory can be inspected, and review or delete saved reports if the inventory is sensitive. <br>
Risk: Public ClawHub pages, search results, or advisory feeds may be unavailable or incomplete during a run. <br>
Mitigation: Treat findings as triage signals, verify important flags manually, and note skipped advisory checks instead of treating them as a clean result. <br>
Risk: The full workflow may write a local audit report for history. <br>
Mitigation: Confirm the report location and retention expectations before scheduled use, especially on shared workspaces. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ordo-tech/skill-fleet-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/ordo-tech) <br>
- [ClawHub security advisories](https://clawhub.com/security/advisories) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown fleet health report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports installed skill names, versions, publishers, status labels, and suggested actions; the full workflow may save a local Markdown report for audit history.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
