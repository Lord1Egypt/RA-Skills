## Description:

Guides agents through bounded adversarial review of non-trivial decisions to reduce overconfident mistakes in architecture, code, deployment, migration, and other high-risk work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when correctness matters more than speed, especially for architecture choices, non-trivial code changes, production deployments, data migrations, and irreversible operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can add review effort, latency, or sub-agent usage to non-trivial decisions.

Mitigation: Apply it to decisions where correctness matters more than speed, and stop on minor repeated findings, after three rounds, or when the user overrides.

Risk: The skill is written in Chinese, which may reduce reviewability for users who do not read Chinese.

Mitigation: Use a translated or bilingual version before installation or operational use when the operator cannot read Chinese.

Risk: Fresh-context or cross-model review can expose artifacts beyond the main agent context if used without care.

Mitigation: Send only the artifact and contract to the reviewer, omit the author's claim and reasoning, and obtain explicit user authorization for each cross-model review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/qqyougit-doubt-driven-development)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown checklists, adversarial review prompts, findings classifications, and concise decision notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bounded review loop with up to three rounds unless the user overrides or the artifact is decomposed.]

## Skill Version(s):

3.0.1 (source: server release evidence; artifact frontmatter is 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
