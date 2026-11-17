## Description:

Queries Qixin for basic enterprise registration information, including unified social credit code, legal representative, registered capital, operating status, suspected controller, taxpayer qualification, and social insurance headcount.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llx-26](https://clawhub.ai/user/llx-26)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business, supplier, procurement, bid, and contract-review teams use this skill to check company registration details and operating status before relying on a business counterparty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names or IDs submitted through the skill are sent to Qixin's external API.

Mitigation: Confirm the user or organization is allowed to send those business identifiers to Qixin before querying.

Risk: The QXBENT_API_TOKEN is a credential required for API access.

Mitigation: Store it only in an environment variable or managed secret store, avoid committing it to files, and rotate it if exposure is suspected.

Risk: Fuzzy company-name lookup may return an unintended company record.

Mitigation: Verify the returned ename and key identifiers before using the result for onboarding, bid, supplier, or contract decisions.

Risk: Dependency installation relies on npm package resolution for axios without a reviewed lockfile in the artifact.

Mitigation: Use a reviewed lockfile or pinned dependency versions in controlled deployments.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/llx-26/skills/qxb-gs-basic-info)
- [getGsBasicInfo reference](references/getGsBasicInfo.md)
- [Qixin API token quota page](https://www.qixin.com/app-center/home?route=skill-quota)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, configuration]

**Output Format:** [Structured enterprise records returned by API calls, with usage guidance and setup commands in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, network access to Qixin, and the QXBENT_API_TOKEN environment variable.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
