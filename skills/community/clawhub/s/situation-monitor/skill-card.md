## Description:

Triages Discord activity and Kubernetes incidents into ranked situation reports with fixture-first demos, live Discord and Apify intake, Contextual-grounded runbooks, Redis-backed memory, Friendli-powered drafting, and approval-gated outbound actions.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[mohnishb-ai](https://clawhub.ai/user/mohnishb-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and operations teams use this skill to summarize noisy Discord activity, triage Kubernetes incidents, and produce concise reports with prioritized follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled Kubernetes disruption and deletion tooling can affect live clusters.

Mitigation: Install in a test or tightly controlled environment, remove or isolate 02-incidents.sh, and restrict Kubernetes credentials to read-only monitoring permissions.

Risk: Live intake and state storage can retain operational or chat data.

Mitigation: Use approved fixture files and set explicit retention and permission controls for Redis and local state.

Risk: The Apify actor uses a Node dependency tree that may change over time.

Mitigation: Update or review Node dependencies before running the actor.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohnishb-ai/skills/situation-monitor)
- [Situation Monitor README](README.md)
- [Situation Monitor OpenClaw Admin Install](docs/openclaw_admin_install.md)
- [KubeWatch Runbooks](docs/context/)
- [Google Cloud Status Incidents API](https://status.cloud.google.com/incidents.json)
- [GitHub Status Incidents API](https://www.githubstatus.com/api/v2/incidents/unresolved.json)
- [Kubernetes GitHub Issues API](https://api.github.com/repos/kubernetes/kubernetes/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, shell command examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include executive summaries, urgent threads, direct asks, decisions, deadlines, source citations, incident priorities, remediation steps, and draft replies.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence; pyproject.toml and package.json list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
