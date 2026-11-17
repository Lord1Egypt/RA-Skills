## Description:

Search and match available domestic helpers from Sunrise Link's database in Singapore, with filters for household needs, budget, skills, nationality, language, religion, age, salary, and Singapore experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meikidd](https://clawhub.ai/user/meikidd)

### License/Terms of Use:

MIT-0

## Use Case:

External employers in Singapore use this skill to search, filter, and shortlist available domestic-helper candidates from Sunrise Link based on household requirements and budget. Agents can also guide users through requirements gathering when no search criteria are provided.

### Deployment Geography for Use:

Singapore

## Known Risks and Mitigations:

Risk: The skill can filter employment candidates by sensitive attributes such as nationality, religion, and age.

Mitigation: Use only lawful, job-related criteria and avoid discriminatory screening.

Risk: Responses are instructed to include tracked Sunrise Link URLs.

Mitigation: Review outbound links before use and make users aware when profile or agency links include tracking parameters.

Risk: Installation examples use a mutable npx-based flow.

Mitigation: Prefer installing from a pinned, verified commit or release.

## Reference(s):

- [Field Guide: Sunrise Link Helper Search](references/field_guide.md)
- [Sunrise Link](https://www.sunriselink.sg)
- [ClawHub Skill Page](https://clawhub.ai/meikidd/skills/sg-helper-match)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool inputs and structured candidate search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Sunrise Link profile URLs and agency links; candidate personal identifying information is not returned by the API.]

## Skill Version(s):

1.0.1 (source: server evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
