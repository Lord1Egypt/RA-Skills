## Description:

Creates an end-to-end self-guided trip plan, including requirements capture, multi-source research, itinerary decisions, Markdown travel documents, interactive Todo dashboards, optional sync, and static deployment guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to turn a destination or partial booking into a structured independent-travel plan, printable itinerary, actionable Todo list, and optional shared trip dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional cloud sync patterns could expose private trip data if room IDs are guessable or sharing controls are weak.

Mitigation: Prefer the default localStorage mode for private use; when cloud sync is needed, use private authenticated sync and high-entropy room IDs.

Risk: Static browser code can expose GitHub personal access tokens or JSONBin master keys if those options are copied into a public page.

Mitigation: Do not embed long-lived credentials in static client code; place credentialed writes behind an authenticated backend or private service.

Risk: Generated itineraries and dashboards can contain confirmation numbers, payment details, or personal travel information.

Mitigation: Remove confirmation numbers, card details, personal identifiers, and sensitive itinerary details before publishing or sharing generated pages.

Risk: Optional Docker or compose setup for third-party research tools may introduce operational or supply-chain risk.

Mitigation: Review Docker images, compose files, and network exposure before running third-party services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dengjiawei1226/skills/trip-planner-0to1)
- [Workflow checklist](references/workflow-checklist.md)
- [Research prompts](references/research-prompts.md)
- [Itinerary template](references/templates/itinerary-template.md)
- [Interactive dashboard template](references/templates/index-skeleton.html)
- [Todo sync template](references/templates/todo-sync.js)
- [Cloudflare Workers sync notes](references/cloudflare-workers-sync.md)
- [Self-hosted sync notes](references/self-host-sync.md)
- [xiaohongshu MCP](https://github.com/xpzouying/xiaohongshu-mcp)
- [Leaflet](https://leafletjs.com/)
- [Lucide](https://lucide.dev/)
- [Cloudflare Workers](https://developers.cloudflare.com/workers/)
- [JSONBin.io](https://jsonbin.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown itinerary drafts, HTML and JavaScript templates, checklist guidance, and shell or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional local-only or cloud-backed Todo synchronization patterns.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
