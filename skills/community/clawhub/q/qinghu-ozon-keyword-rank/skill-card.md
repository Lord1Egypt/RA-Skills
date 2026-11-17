## Description:

Helps agents query and summarize Ozon trending keywords by category, reporting period, search metrics, and sales indicators through Qinghu data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Marketplace sellers and analysts use this skill to find and compare Ozon trending keywords across categories and reporting periods before choosing search or product opportunities.

### Deployment Geography for Use:

Global (queries Ozon marketplace data through the Qinghu China service)

## Known Risks and Mitigations:

Risk: Automatic installation or upgrading of qhkit and Node can change the user's environment.

Mitigation: Have the user review and pin the tooling before installation; avoid automatic global installs or shell-profile changes.

Risk: Configuring a Qinghu API token can expose credentials if handled carelessly.

Mitigation: Provide the token through a controlled environment variable and avoid displaying or storing it in shared files.

Risk: Qinghu API queries can incur charges that rise with result volume.

Mitigation: Estimate costs and obtain user approval before paid calls, especially for large result sets.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-ozon-keyword-rank)
- [Qinghu qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with keyword metrics and source period]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on requested filters and the latest available Qinghu data.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
