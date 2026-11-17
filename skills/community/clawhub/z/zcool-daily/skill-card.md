## Description:

Automatically fetches popular ZCOOL homepage design works and generates a daily recommendation report with links, categories, highlight descriptions, and trend counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heihu123](https://clawhub.ai/user/heihu123)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, content curators, and social media operators use this skill to collect current ZCOOL popular works and prepare a concise daily recommendation digest. The generated report helps readers scan work links, design categories, short highlights, and category trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts ZCOOL and linked work pages while generating the report.

Mitigation: Run it only in environments where outbound access to ZCOOL and fetched work pages is acceptable.

Risk: The generated same-day report file may overwrite an existing file in the configured output directory.

Mitigation: Use a dedicated output directory or review existing zcool_daily/zcool_{date}.txt files before running.

Risk: Runtime behavior depends on ordinary third-party Python packages and the current ZCOOL page structure.

Mitigation: Install dependencies in a virtual environment, consider pinning package versions, and review output after site changes.

## Reference(s):

- [Output Example](references/output-example.md)
- [ZCOOL Homepage](https://www.zcool.com.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands]

**Output Format:** [Markdown-style daily report saved as a text file and printed to standard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or overwrites zcool_daily/zcool_{date}.txt for the current date.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
