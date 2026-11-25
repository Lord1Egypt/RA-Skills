## Description:

Collects the current public Weibo hot list, including ranks, heat values, topic links, and CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystery77777777](https://clawhub.ai/user/mystery77777777)

### License/Terms of Use:

MIT-0

## Use Case:

People who follow public Weibo trends can retrieve the current ranked hot list and export it as CSV. The skill returns structured results with titles, heat values, categories, and topic links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates this release suspicious and covered only 33.3% of components, leaving uninspected behavior unassessed.

Mitigation: Review the complete source and perform a full security scan before execution.

Risk: The default service URL uses plain HTTP, so platform access tokens may be transmitted without transport encryption.

Mitigation: Configure an HTTPS service URL and keep access tokens private.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mystery77777777/skills/wb-hot)

## Skill Output:

**Output Type(s):** [JSON data, CSV files, Guidance]

**Output Format:** [JSON results and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current ranked hot list with titles, keywords, heat values, labels, categories, and links; CSV includes a summary and item details.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
