## Description:

Skills Finder searches ClawHub and Skills.sh in real time to recommend, list, and install agent skills across multilingual queries and multi-step tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welliu](https://clawhub.ai/user/welliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find, compare, list, and install skills from ClawHub and Skills.sh for multilingual requests and chained tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run mutable npm tools through npx and install agent skills without strong version pinning or confirmation.

Mitigation: Use it in a restricted workspace, avoid exposing secrets to the process environment, and prefer pinned or preinstalled marketplace CLIs before search, list, or install operations.

Risk: The install workflow can add skills from external marketplaces.

Mitigation: Review and scan selected skills before deployment, especially when installing from live marketplace results.

Risk: Search and list results depend on external marketplace availability and rate limits.

Mitigation: Treat marketplace failures or rate-limit messages as expected operational conditions and retry or narrow the source when needed.

## Reference(s):

- [ClawHub Skills Finder listing](https://clawhub.ai/welliu/skills/skills-finder)
- [Evaluation prompts](artifact/evals/evals.json)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Terminal text and Markdown guidance with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on live marketplace CLIs, network access, and rate limits.]

## Skill Version(s):

1.6.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
