## Description: <br>
Connects Gmail, Calendar, Drive, Atlassian, Notion, GitHub, Salesforce, and other enterprise tools through a Venn MCP endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninonano64](https://clawhub.ai/user/ninonano64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to connect an agent to Venn-managed SaaS accounts, discover available services, summarize work items, and perform authenticated workflows across connected enterprise tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow installs an unpinned third-party CLI. <br>
Mitigation: Review before installing, proceed only if the publisher, Venn service, and external CLI fork are trusted, and prefer a pinned or signed release when available. <br>
Risk: OAuth-connected services can expose broad work-account data. <br>
Mitigation: Supervise OAuth scopes and explicitly confirm setup, write, and multi-step actions against connected work systems. <br>
Risk: Broad activation rules can trigger connected SaaS lookups for service-related requests. <br>
Mitigation: Discover and describe tools before execution, confirm write operations, and return only the necessary fields to the user. <br>


## Reference(s): <br>
- [Venn](https://venn.ai) <br>
- [Venn OpenClaw Assistant Setup](https://app.venn.ai/assistants/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/ninonano64/venn-nino) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and JSON arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require OAuth authentication and a VENN_UNIVERSAL_URL; connected service results should be summarized with only necessary fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
