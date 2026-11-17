## Description:

Searchable knowledge base that captures and cross-references shared URLs, saves structured source summaries with claims, quotes, analysis, tags, and freshness tracking, and helps retrieve connections, conflicts, and reading queue items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[don-gbot](https://clawhub.ai/user/don-gbot)

### License/Terms of Use:

ISC

## Use Case:

External users and developers use this skill to turn shared links into a persistent local research library with searchable summaries, cross-references, conflict checks, and queue management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared URLs and related analysis are saved as long-term local knowledge by default.

Mitigation: Avoid sharing private, internal, or sensitive URLs while the skill is active unless persistent local storage is intended; review and delete stored source files when needed.

## Reference(s):

- [ClawHub Source Library Skill Page](https://clawhub.ai/don-gbot/skills/source-library)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown files and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists source summaries under life/source and a reading queue under data/source-queue.json.]

## Skill Version(s):

2.1.1 (source: server release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
