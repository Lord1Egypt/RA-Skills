## Description:

Guides users in Chinese through selecting a steering gear product, collecting design parameters, calculating values, and creating a jixietools.com guest drawing order for CAD output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realsanyu](https://clawhub.ai/user/realsanyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and engineering teams use this skill to generate steering gear CAD drawing requests by choosing a product, entering parameters step by step, reviewing calculated results, and tracking drawing generation through jixietools.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends steering-gear design inputs to jixietools.com and creates a guest production sheet there.

Mitigation: Avoid using confidential or sensitive engineering parameters unless sharing them with that service is acceptable.

Risk: The workflow polls a third-party guest status endpoint and returns generated drawing links.

Mitigation: Review service links and generated drawing outputs before relying on them for engineering, purchasing, or manufacturing decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realsanyu/skills/steering-gear)
- [jixietools.com API base](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API calls]

**Output Format:** [Chinese Markdown with tables, inline shell commands, JSON examples, progress updates, and service links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides one parameter at a time, preserves calculation filenames for incremental updates, and polls the guest production sheet status every 5 seconds.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
