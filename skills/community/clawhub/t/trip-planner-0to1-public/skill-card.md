## Description:

Trip Planner 0to1 Public guides an agent through end-to-end independent travel planning, from requirements gathering and multi-source research to Markdown itineraries, multi-page trip websites, Todo sync, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226)

### License/Terms of Use:

MIT-0

## Use Case:

Travel planners and agent users use this skill to turn an initial destination or flight into a structured trip plan, validated itinerary, operational travel website, Todo checklist, and deployment package. It is designed for independent travel scenarios such as island trips, Japan itineraries, European road trips, and North or South American road travel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can invoke authenticated social-media MCP tools and mutable third-party npm or Docker components.

Mitigation: Pin and review third-party MCP, npm, and Docker components before use, and avoid running unreviewed update or install commands automatically.

Risk: Optional cloud Todo sync patterns can expose travel data or secrets if credentials are placed in browser JavaScript.

Mitigation: Prefer local-only Todo sync by default, and do not put GitHub or JSONBin secrets in client-side JavaScript.

Risk: Deployment, Docker, sudo, and update commands can change local or hosted environments.

Mitigation: Treat each deployment, Docker, sudo, and update command as an explicit approval step before execution.

Risk: Travel recommendations can become inaccurate when web, map, schedule, or social-media sources are stale or promotional.

Mitigation: Cross-check key travel facts with at least two sources and confirm critical routes, schedules, reservations, and coordinates against authoritative sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dengjiawei1226/skills/trip-planner-0to1-public)
- [README](README.md)
- [Workflow checklist](references/workflow-checklist.md)
- [Research prompt templates](references/research-prompts.md)
- [Cloudflare Workers KV sync guide](references/cloudflare-workers-sync.md)
- [Self-hosted sync guide](references/self-host-sync.md)
- [Itinerary template](references/templates/itinerary-template.md)
- [Command center HTML skeleton](references/templates/index-skeleton.html)
- [Itinerary page HTML skeleton](references/templates/itinerary-page-skeleton.html)
- [Route patch script](references/templates/patch-trip-page-v2.js)
- [Todo sync template](references/templates/todo-sync.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown travel plans, HTML and JavaScript page templates, shell commands, configuration snippets, and concise operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include itinerary files, Todo checklists, travel website pages, route data, deployment instructions, and optional sync setup.]

## Skill Version(s):

2.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
