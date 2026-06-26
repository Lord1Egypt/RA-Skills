## Description: <br>
Enrich, search, and manage company and professional data, lists, saved searches, and signals using the Specter intelligence platform via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FroeMic](https://clawhub.ai/user/FroeMic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, sales teams, and deal-sourcing users can use this skill to operate the Specter CLI for company and people enrichment, list management, saved-search retrieval, and talent or investor-interest signal lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Specter API keys may grant access to account data if exposed or over-privileged. <br>
Mitigation: Use revocable or least-privileged API keys where possible, store them in environment variables, and rotate them if exposure is suspected. <br>
Risk: Company, people, LinkedIn, email, and file-input workflows can involve confidential, regulated, or personal data. <br>
Mitigation: Submit only data approved for Specter processing and avoid regulated or confidential inputs unless organizational policy allows it. <br>
Risk: Delete and remove commands can affect saved searches, lists, or list contents. <br>
Mitigation: Confirm exact Specter IDs and intended scope before running remove or delete commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FroeMic/specter) <br>
- [Specter API Console](https://app.tryspecter.com/settings/api-console) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI examples may request JSON, table, or CSV output from Specter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
