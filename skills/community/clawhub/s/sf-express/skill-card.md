## Description: <br>
Use SF Express (顺丰速运) for shipment tracking, delivery anomaly triage, e-commerce seller/customer handoffs, shipping guidance, service-type comparison, outlet lookup, and delivery-time or fee estimation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, customer-support agents, e-commerce sellers, and operations teams use this skill to understand SF Express shipment status, triage delivery anomalies, compare shipping services, estimate fees or timing, and prepare practical handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local CLI can store tracking history, subscriptions, address records, encrypted helper files, and privacy exports under ~/.openclaw/data/sf-express. <br>
Mitigation: Use persistence only when needed, disclose the storage paths for privacy-sensitive workflows, and use the privacy info, export, and clear commands to review or remove local data. <br>
Risk: Live shipment queries depend on a user-configured endpoint, and shipment numbers can be sensitive on shared systems. <br>
Mitigation: Use only trusted HTTPS tracking endpoints, avoid entering sensitive shipment numbers on shared systems unless necessary, and treat mock output only as labeled demo data. <br>
Risk: Fee and delivery-time estimates may be approximate when not backed by live SF Express data or user-provided carrier data. <br>
Mitigation: State assumptions, avoid promising arrival times or prices, and direct users to official SF Express channels for binding shipping actions or final quotes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/sf-express) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cautious estimates, anomaly triage summaries, privacy/storage notes, and CLI command suggestions.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
