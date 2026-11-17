## Description:

Publish AI agent skills to GitHub and multiple skill registries in one workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orbisz](https://clawhub.ai/user/orbisz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to publish or update AI agent skills across GitHub, skills.sh, ClawHub, and skillsmp.com from one workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad repository publishing power, including commits, pushes, remote changes, force-pushes, and registry publication.

Mitigation: Review the exact repository, remote URL, branch, staged file list, and target registries; require explicit confirmation before any commit, push, remote change, force-push, or registry publish.

Risk: Running the skill in a directory with secrets or unrelated files could expose or publish unintended content.

Mitigation: Run it only in the intended skill repository after reviewing contents and scanning for secrets or unrelated files.

Risk: Persistent repository mapping and self-evolution behavior may retain project paths or suggest future modifications across runs.

Mitigation: Review, disable, or remove repo-map and diary/self-evolution behavior before installation in shared or sensitive environments.

## Reference(s):

- [Skill source](artifact/SKILL.md)
- [Repository mapping reference](artifact/references/repo-map.json)
- [ClawHub skill page](https://clawhub.ai/orbisz/skills/skill-publish-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commit messages, changelog text, repository URLs, and registry publication URLs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
