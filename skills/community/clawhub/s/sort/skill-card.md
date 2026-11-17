## Description:

Sort files, lines, and columns with custom ordering, deduplication, ranking, shuffling, frequency analysis, and basic statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use Sort to process local text, CSV, JSON, and tabular files for ordering, deduplication, ranking, frequency reports, and basic file statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that one JSON sorting fallback can turn crafted input into Python code execution.

Mitigation: Review before installing, prefer systems with jq available, and avoid using the json command on untrusted filenames or keys.

Risk: The skill keeps a persistent local operation history containing processed filenames and metadata.

Mitigation: Do not use it on sensitive paths unless retaining an audit trail at ~/.local/share/sort/history.log is acceptable.

## Reference(s):

- [Sort skill page](https://clawhub.ai/ckchzh/skills/sort)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown guidance with shell command examples and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands read local files and print sorted, deduplicated, ranked, shuffled, frequency, statistics, CSV, or JSON results to standard output.]

## Skill Version(s):

3.0.2 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
