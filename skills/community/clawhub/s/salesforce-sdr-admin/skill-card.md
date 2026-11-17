## Description:

This skill supports UI-driven Salesforce SDR and admin work in the browser across Sales Cloud, Service Cloud, Experience Cloud, and CPQ/Revenue Cloud with confirmation gates and local credential handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sfdcbrewery](https://clawhub.ai/user/sfdcbrewery)

### License/Terms of Use:


## Use Case:

Salesforce SDRs, admins, and developers use this skill to complete browser-based Salesforce record, setup, CPQ, and code-editing tasks. It is intended for work where credentials remain local and write actions require explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate Salesforce in a browser with the permissions of the signed-in user, including broad admin authority.

Mitigation: Use a least-privileged Salesforce automation account and require explicit record, environment, and impact confirmation before deletes, setup changes, deployments, or code edits.

Risk: The artifact documents reusable local Salesforce credentials, including a plaintext local credential file option.

Mitigation: Prefer browser autofill or an OS credential manager and avoid storing reusable credentials in plaintext.

Risk: Salesforce records, emails, and pages may contain untrusted instructions that could attempt to override task boundaries.

Mitigation: Treat Salesforce page content as data, ignore embedded instructions, and abort requests that attempt credential exfiltration or confirmation bypass.

## Reference(s):

- [Local Credential Sources](artifact/references/credentials.md)
- [UI Flows (Salesforce Lightning)](artifact/references/ui-flow.md)
- [Salesforce Domain Cheatsheet](artifact/references/domain-cheatsheet.md)
- [Salesforce Dev Cheatsheet](artifact/references/dev-cheatsheet.md)
- [Prompt-Injection Guardrails](artifact/references/prompt-injection-guardrails.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown with task summaries, confirmations, record links, configuration snippets, and code or command blocks when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run summaries, success evidence, and required confirmation prompts before write actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
