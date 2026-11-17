## Description:

Searches Shopee's T+1 brand database by category or brand name and ranks brands by product count, recent sales, revenue, or shop count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and analysts use this skill to find and compare brands in supported Shopee markets by category, name, and sales-related rankings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading the third-party qhkit package and changing local Node or PATH settings can affect the user's environment.

Mitigation: Review and approve installation or upgrades separately; prefer a trusted, pre-provisioned or pinned qhkit version.

Risk: A qhkit API token may be stored locally or exposed if pasted into chat.

Mitigation: Use the platform's secure secret handling and avoid sharing long-lived tokens in chat.

Risk: Brand lookups and related calls consume paid Qinghu credits; retries may also incur charges.

Mitigation: Check current pricing and obtain the user's approval before paid calls; avoid repeated speculative retries.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-brand-list)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Brief written findings with a small preview; a tabular file for 10 or more records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shopee brand data is T+1; findings identify the site, period, and sample size. Paid API calls require user approval.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
