## Description: <br>
Review Agent is a pre-meeting review coach for Lark/Feishu or WeCom that ingests drafts, proposals, plans, or agendas, runs a four-pillar review with responder simulation, and guides requesters through findings before producing a decision brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinghaojia](https://clawhub.ai/user/yinghaojia) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees and teams use this skill to prepare higher-quality meeting materials before a decision discussion. It helps requesters clarify background, supporting materials, decision framework, and intended ask, then produces a six-section decision brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process confidential drafts, responder profiles, conversations, dissent notes, and summaries. <br>
Mitigation: Deploy only where the required confidentiality controls are in place, restrict local archive access, and avoid submitting materials that should not be stored or sent to configured model providers. <br>
Risk: Bot document and drive permissions can expose more workspace data than a review session requires. <br>
Mitigation: Grant only the minimum Feishu/Lark or WeCom scopes needed for the deployment and review those scopes before production use. <br>
Risk: The full architecture depends on per-peer isolation in Feishu/Lark or WeCom; other channels fall back to shared main-agent mode. <br>
Mitigation: Use Feishu/Lark or WeCom for normal deployment, and avoid shared-channel use when requesters' materials must remain isolated. <br>
Risk: The package references an external installer and OpenClaw patch outside the reviewed artifact. <br>
Mitigation: Review the external installer and patch before running them, and verify the installed OpenClaw configuration after setup. <br>
Risk: Delivery targets can send summaries and final materials to Lark, email, Google Drive, or local archives. <br>
Mitigation: Audit delivery_targets.json before enabling the skill and confirm every destination, role, and payload type is intentional. <br>


## Reference(s): <br>
- [Review Agent ClawHub page](https://clawhub.ai/yinghaojia/review-agent) <br>
- [README](README.md) <br>
- [Agent Persona](references/agent_persona.md) <br>
- [Four Pillars](references/four_pillars.md) <br>
- [Annotation Schema](references/annotation_schema.md) <br>
- [Summary Template](references/summary_template.md) <br>
- [Delivery Backends](references/delivery/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON status output, and command-line workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces normalized review materials, findings, revised drafts, changelogs, verdict JSON, and final decision briefs in session workspaces.] <br>

## Skill Version(s): <br>
2.1.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
