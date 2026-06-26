## Description: <br>
Creates an end-to-end independent travel planning workflow covering requirements gathering, multi-source research, itinerary decisions, Markdown trip documents, multi-page trip websites, Todo sync, and deployment options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel planners and agent users use this skill to turn early trip details into a researched itinerary, operational checklist, multi-page trip site, and deployment or sync plan. It is suited to independent travel scenarios such as island trips, Japan trips, Europe road trips, and Americas road trips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud or browser-based Todo sync can expose private trip data or credentials if tokens, JSONBin master keys, or booking details are embedded in client-side code. <br>
Mitigation: Keep sync local by default, store secrets outside browser JavaScript, and redact booking references, policy numbers, and other sensitive travel details before sharing or deploying pages. <br>
Risk: Third-party MCP packages that receive login cookies can expose account data if they are not reviewed and pinned. <br>
Mitigation: Pin and review third-party MCP packages before use, grant only the minimum required access, and avoid providing cookies to untrusted packages. <br>
Risk: Silent version-check or update behavior can alter the local environment without clear user review. <br>
Mitigation: Disable or remove silent update-check behavior, and require explicit user confirmation before running update commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dengjiawei1226/trip-planner-0to1-public) <br>
- [Workflow checklist](references/workflow-checklist.md) <br>
- [Research prompts](references/research-prompts.md) <br>
- [Cloudflare Workers sync](references/cloudflare-workers-sync.md) <br>
- [Self-host sync](references/self-host-sync.md) <br>
- [Itinerary template](references/templates/itinerary-template.md) <br>
- [Todo sync template](references/templates/todo-sync.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown trip plans, HTML and JavaScript files, checklists, configuration snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployment links and Todo sync setup; review sensitive booking, token, and itinerary data before publishing.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
