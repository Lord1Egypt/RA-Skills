## Description:

Reads local text files and automatically detects GBK or UTF-8 encoding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[delicate314](https://clawhub.ai/user/delicate314)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to read local text-oriented files, especially Chinese Windows files that may use GBK encoding. It can also extract text from DOCX and text-based PDF files when the required Python packages are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically install unpinned Python packages when reading DOCX or PDF files.

Mitigation: Use a controlled Python environment such as a virtual environment or container, and preinstall reviewed, pinned versions of python-docx and pypdf.

Risk: Local file contents are printed to stdout and may appear in agent transcripts or logs.

Mitigation: Avoid using the skill on credentials, private records, or other sensitive files unless that exposure is acceptable.

## Reference(s):

- [Python downloads](https://www.python.org/downloads/)
- [Miniconda documentation](https://docs.conda.io/en/latest/miniconda.html)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text written to stdout, with errors and encoding notices written to stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a single local file path per invocation; very large files may be truncated.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
