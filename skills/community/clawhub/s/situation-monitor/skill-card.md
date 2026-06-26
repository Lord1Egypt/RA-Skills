## Description: <br>
Triages Discord activity and Kubernetes incidents into ranked situation reports with fixture-first demos, live Discord and Apify intake, Contextual-grounded runbooks, Redis-backed memory, Friendli-powered drafting, and approval-gated outbound actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohnishb-ai](https://clawhub.ai/user/mohnishb-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and operations teams use this skill to summarize noisy Discord activity, triage Kubernetes incidents, and turn operational signals into prioritized reports and safe follow-up drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Kubernetes access and the incident drill script can affect real infrastructure. <br>
Mitigation: Use fixture mode or a disposable demo cluster by default, and do not run 02-incidents.sh against real infrastructure. <br>
Risk: Live cluster scans may expose or act on sensitive operational state. <br>
Mitigation: Provide least-privilege read-only Kubernetes credentials for live scans. <br>
Risk: Discord ingestion can capture personal or private channel content. <br>
Mitigation: Use bot-visible channels only, avoid private Discord channels unless users approved ingestion, and prefer fixture data for demos. <br>
Risk: Outbound messages could be sent without an appropriate approval workflow. <br>
Mitigation: Keep outbound posting blocked until a real approval flow is configured. <br>


## Reference(s): <br>
- [Situation Monitor README](artifact/README.md) <br>
- [Situation Monitor Skill Definition](artifact/SKILL.md) <br>
- [OpenClaw Admin Install Guide](artifact/docs/openclaw_admin_install.md) <br>
- [KubeWatch Runbooks](artifact/docs/context/) <br>
- [GCP Status Incidents API](https://status.cloud.google.com/incidents.json) <br>
- [GitHub Status Unresolved Incidents API](https://www.githubstatus.com/api/v2/incidents/unresolved.json) <br>
- [Kubernetes Critical Bug Issues API](https://api.github.com/repos/kubernetes/kubernetes/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and plain text drafts, with optional shell commands and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can be printed or saved to a local Markdown path; outbound posting stays blocked until approval is configured.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
