## Description: <br>
UI-driven Salesforce SDR and admin execution across Sales Cloud, Service Cloud, Experience Cloud, and CPQ/Revenue Cloud for browser-based Salesforce tasks with strict confirmation and secure local credential handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sfdcbrewery](https://clawhub.ai/user/sfdcbrewery) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Salesforce SDRs, admins, and developers use this skill to operate Salesforce through the browser for lead, opportunity, case, quote, setup, and Salesforce development tasks. It is intended for human-supervised workflows where write actions are reviewed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform powerful Salesforce admin, development, and data-change actions through a browser. <br>
Mitigation: Use a least-privileged Salesforce account, prefer sandbox environments for risky changes, and require explicit review before create, update, delete, setup, or deployment actions. <br>
Risk: Salesforce records, pages, emails, or attachments may contain untrusted instructions that conflict with the user's request. <br>
Mitigation: Treat in-page content as data, ignore embedded instructions, and continue only when the requested task and intended changes are clear. <br>
Risk: Local credentials and browser profiles can expose Salesforce access if mishandled. <br>
Mitigation: Use local-only credential sources, never paste secrets into chat, and protect credential files and browser profiles. <br>


## Reference(s): <br>
- [Local Credential Sources](references/credentials.md) <br>
- [UI Flows (Salesforce Lightning)](references/ui-flow.md) <br>
- [Salesforce Domain Cheatsheet](references/domain-cheatsheet.md) <br>
- [Salesforce Dev Cheatsheet](references/dev-cheatsheet.md) <br>
- [Prompt-Injection Guardrails](references/prompt-injection-guardrails.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown summaries with browser task results, record URLs, proposed changes, and code or configuration snippets when relevant.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write actions require explicit user confirmation; results should include success evidence such as a toast, record URL, or confirmation text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
