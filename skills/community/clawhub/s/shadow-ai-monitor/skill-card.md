## Description: <br>
Shadow AI Monitor generates an enterprise dashboard for tracking employee AI tool usage, data exposure risks, and PIPEDA compliance, with interactive drill-downs, compliance analysis, and PDF export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TechCodeCrafter](https://clawhub.ai/user/TechCodeCrafter) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Security, compliance, and technology teams use this skill to generate local reports that summarize AI tool usage, data exposure risk, PIPEDA compliance posture, and remediation recommendations. Consultants and sales teams can also use its demo data generator for AI governance presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate reports about employee AI-tool usage, which may be sensitive workplace-monitoring data. <br>
Mitigation: Use it only with legal, HR, privacy, security, and organizational authorization, and store generated reports in approved sensitive-data locations. <br>
Risk: The generated dashboard loads Chart.js from a CDN, which may be unsuitable for strict offline or restricted environments. <br>
Mitigation: Avoid the CDN-backed dashboard in strict offline environments or replace the CDN dependency with an approved local asset before use. <br>
Risk: The documentation describes optional WhatsApp delivery of metrics, which could expose sensitive monitoring results outside approved channels. <br>
Mitigation: Do not send metrics to WhatsApp or other external channels without legal, HR, privacy, and security approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TechCodeCrafter/shadow-ai-monitor) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/TechCodeCrafter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON data files and local HTML dashboards, with Markdown usage guidance and shell commands in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates shadow-ai-data.json and shadow-ai-dashboard.html locally; the dashboard can be exported to PDF from a browser.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
