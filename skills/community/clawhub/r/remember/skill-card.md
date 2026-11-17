## Description:

Curate persistent memory that actually helps. Filter what matters, organize by function, decay what doesn't.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to decide what information an agent should persist, how to organize memory files, and how to prune stale or misleading entries over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain secrets, credentials, health details, or sensitive personal and business facts.

Mitigation: Avoid storing sensitive information unless the user explicitly wants it remembered, and honor forget requests and privacy boundaries.

Risk: Stale or incorrect memory can mislead future agent behavior.

Mitigation: Apply the documented review, contradiction-resolution, and pruning process before relying on older memory.

## Reference(s):

- [Memory Categories](artifact/categories.md)
- [Memory Consolidation Process](artifact/consolidation.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with memory organization templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; guidance may be used to create or maintain persistent memory files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
