## Description:

Agent skill recommender. Input a user need, task description, or existing skill list; output best matching skills, install rationale, duplicate/merge candidates, and gaps for new skill briefs. Runtime-neutral and not tied to one agent platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find the best matching skills in an existing collection, identify duplicate or overlapping skills, and decide whether to reuse, extend, merge, or create a skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Node.js helpers read SKILL.md files from the skills directory supplied by the user.

Mitigation: Run the helpers only against intended skill directories and avoid pointing them at unrelated private workspaces.

Risk: Recommendations are lightweight and keyword-based, with several templates and examples written in Chinese.

Mitigation: Review ranked matches and rationale before acting on reuse, merge, or build-new decisions, especially for multilingual or ambiguous requests.

## Reference(s):

- [Recommendation Rules](references/recommendation-rules.md)
- [Output Schema](references/output-schema.md)
- [Dedup / Avoid-Rebuild Mode](references/dedup-mode.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown responses and JSON from local helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked scores, match labels, rationale, boundaries, overlap groups, and next-step guidance.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
