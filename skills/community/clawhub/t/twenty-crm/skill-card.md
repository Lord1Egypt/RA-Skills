## Description:

Interact with Twenty CRM (self-hosted) via REST/GraphQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhumanj](https://clawhub.ai/user/jhumanj)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to query and manage a self-hosted Twenty CRM workspace through REST and GraphQL helpers, including company lookup, creation, updates, and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-token authority over the configured Twenty CRM can expose or misuse CRM data if the token is broad or mishandled.

Mitigation: Use a narrowly scoped token, store it only in the expected config file with restricted file permissions, prefer HTTPS, and rotate short-lived tokens as needed.

Risk: REST create, update, delete, and destroy helpers can change or permanently remove CRM records.

Mitigation: Review commands and JSON payloads before execution, avoid delete permissions unless required, and test risky operations against non-production data first.

Risk: The config helper uses a hardcoded local path for the Twenty CRM environment file.

Mitigation: Review and adjust the config path for the deployment environment before use.

Risk: Object names and endpoints can differ across Twenty workspace metadata and versions.

Mitigation: Confirm object names and endpoint behavior against the target workspace before relying on automated operations.

## Reference(s):

- [Twenty CRM ClawHub release](https://clawhub.ai/jhumanj/skills/twenty-crm)
- [Publisher profile](https://clawhub.ai/user/jhumanj)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute REST or GraphQL requests against the configured Twenty CRM instance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
