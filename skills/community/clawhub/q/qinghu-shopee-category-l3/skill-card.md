## Description:

Looks up Shopee third-level category IDs and names using a second-level category ID, site, and language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and analysts use this skill to find the leaf category IDs and names under a specified second-level category for a supported Shopee site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or upgrade qhkit and Node/npm tooling locally.

Mitigation: Approve installation or upgrades explicitly, use a contained environment, and pin trusted package versions where possible.

Risk: Using the service requires an API token and may persist local configuration.

Mitigation: Review where the token is stored and avoid exposing it in shared logs or files.

Risk: Category lookups are paid API calls.

Mitigation: Check the estimate and obtain user consent before making paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shopee-category-l3)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown with category IDs and names; setup commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Shopee site, language, and second-level category ID; API calls may consume paid credits.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
