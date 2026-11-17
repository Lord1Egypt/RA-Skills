## Description:

Helps teams design staged CI/CD testing, quality gates, and feedback loops for faster, more reliable releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to plan layered tests, quality gates, and release feedback across CI/CD stages, including fast commit checks and regression testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional installation command fetches an unpinned skill package.

Mitigation: Review the command and package before using it.

Risk: Applying deployment or release recommendations without safeguards could affect production systems.

Mitigation: Use only in authorized environments with a reviewed rollout and rollback plan.

## Reference(s):

- [CI/CD pipeline design reference](references/pipeline-design.md)
- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-ci-cd-testing)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Markdown]

**Output Format:** [Markdown pipeline design with test stages, quality gates, and feedback loops]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pipeline IDs use PIPE-XXXX; coverage statements identify their basis and explain uncovered modules.]

## Skill Version(s):

1.8.0 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
