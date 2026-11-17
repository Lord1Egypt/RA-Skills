## Description:

Code review helper that learns from misses by combining checklist checks for security, performance, correctness, and maintainability with scar memory that flags similar patterns in later reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aibenyclaude-coder](https://clawhub.ai/user/aibenyclaude-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to run local checklist-based code reviews, check diffs against recorded review misses, and record new scar patterns after incidents or missed findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scar files contain regex patterns that are executed by Python's regex engine.

Mitigation: Treat scar files as trusted configuration, review patterns before use, and restrict write access to the scar JSONL file.

Risk: Reviewing attacker-controlled code in an interactive terminal may expose users to unsafe terminal output until output escaping is improved.

Mitigation: Run reviews in a controlled terminal, avoid interactive review of untrusted files, or redirect output to a plain log for inspection.

Risk: The tool reads files or diffs supplied by the user and stores local scar records.

Mitigation: Run it only on intended local paths and keep review_scars.jsonl in a location with appropriate project access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aibenyclaude-coder/skills/tetra-scar-code-review)
- [Tetra Genesis project](https://github.com/b-button-corp/tetra-genesis)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Plain text review findings, CLI output, JSONL scar records, and Python data structures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local files or diffs selected by the user and stores review scars in review_scars.jsonl by default.]

## Skill Version(s):

0.1.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
