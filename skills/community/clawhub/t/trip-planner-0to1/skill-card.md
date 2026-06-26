## Description: <br>
Trip Planner 0→1 guides an agent through an end-to-end self-guided travel planning workflow, from requirements gathering and multi-source research to itinerary Markdown, an interactive todo dashboard, optional sync, and static deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to produce structured self-guided trip plans, day-by-day itinerary documents, actionable todo lists, and optional shareable dashboards for independent travel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional sync and deployment examples can expose travel data or service credentials if used as written. <br>
Mitigation: Review generated artifacts before syncing or sharing them, keep localStorage mode when possible, avoid placing service credentials in browser code, and add real authentication before deploying a sync backend. <br>
Risk: Public itinerary links can reveal sensitive travel details. <br>
Mitigation: Remove confirmation numbers, order IDs, credit-card details, passport notes, and emergency contacts from any public URL. <br>
Risk: Predictable sync room identifiers can allow unintended access to shared todo data. <br>
Mitigation: Use high-entropy room IDs for any cross-device sync configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dengjiawei1226/trip-planner-0to1) <br>
- [Workflow checklist](artifact/references/workflow-checklist.md) <br>
- [Research prompts](artifact/references/research-prompts.md) <br>
- [Itinerary template](artifact/references/templates/itinerary-template.md) <br>
- [Interactive dashboard template](artifact/references/templates/index-skeleton.html) <br>
- [Todo sync template](artifact/references/templates/todo-sync.js) <br>
- [Cloudflare Workers sync guide](artifact/references/cloudflare-workers-sync.md) <br>
- [Self-hosted sync guide](artifact/references/self-host-sync.md) <br>
- [Leaflet documentation](https://leafletjs.com/) <br>
- [Lucide icons](https://lucide.dev/) <br>
- [Cloudflare Workers documentation](https://developers.cloudflare.com/workers/) <br>
- [JSONBin](https://jsonbin.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with HTML, JavaScript, configuration snippets, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces itinerary documents, todo lists, dashboard files, sync configuration guidance, and deployment steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
