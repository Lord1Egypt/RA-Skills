## Description:

Count words in text, including documented support for totals, unique words, per-line counts, and frequency analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams can use this skill to ask an agent for word-counting help, text-analysis guidance, and simple command examples for documents or pipeline inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public documentation describes options such as unique counts, frequency analysis, per-line output, file input, stopword filtering, and JSON output, while the script evidence only reads stdin and prints a whitespace-split word count.

Mitigation: Treat the release as a basic stdin word counter unless the implementation is updated and retested for the documented advanced options.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/wc-words-tool)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples and optional JSON output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included script evidence only supports a basic stdin word count, despite broader documented options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
