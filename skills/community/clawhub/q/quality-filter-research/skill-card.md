## Description:

Academic paper quality filtering agent with rigorous scoring system and comprehensive audit trail. Filters papers based on relevance and quality criteria for research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nomorecoding](https://clawhub.ai/user/nomorecoding)

### License/Terms of Use:


## Use Case:

Researchers and research workflow agents use this skill to score academic papers for relevance and technical quality, categorize papers as passed or filtered, and preserve an audit trail for manual recall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Filtering decisions are written to a persistent local research log that may contain sensitive paper notes or private review data.

Mitigation: Review the domain and workspace path before use, and avoid submitting sensitive notes unless local storage in that workspace is acceptable.

Risk: The domain value determines the output path for the append-mode audit log.

Mitigation: Choose a clear, expected domain value before running the skill so logs are stored in the intended research directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nomorecoding/skills/quality-filter-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown audit log with scoring rationale and summary statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends filtering sessions to research/{domain}/quality_filtering/quality_filtering_log.md.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
