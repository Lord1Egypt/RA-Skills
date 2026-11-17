## Description:

Queries Ozon public second-level categories by first-level category ID through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Marketplace sellers and analysts use this skill to find Ozon second-level category names and IDs under a known first-level category, with a chosen output language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading qhkit may change local Node tooling or PATH.

Mitigation: Review and approve npm installs, npx runs, Node downloads, PATH changes, and upgrades before execution.

Risk: Configuring a Qinghu API token grants service access.

Mitigation: Confirm token setup and the intended Qinghu account before configuring credentials.

Risk: Category lookups may consume paid Qinghu credits.

Mitigation: Check available pricing, disclose expected credit use, and obtain consent before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-category-l2)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown response with category names and IDs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports credits consumed for paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
