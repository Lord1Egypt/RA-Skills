## Description:

Polishes response letters by transforming defensive or harsh language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, academic authors, and writing-support agents use this skill to turn defensive or harsh draft responses to peer reviewers into courteous academic prose while preserving the author's scientific position.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can read local input files and write or overwrite output files in file-based and interactive modes.

Mitigation: Run it only in a sandboxed workspace and provide only intended workspace-local input and output paths.

Risk: The packaged dependency install step names unnecessary unpinned packages.

Mitigation: Avoid running the pip install step unless dependencies are removed, pinned, or reviewed in a controlled environment.

Risk: Polished responses may over-soften or alter the apparent strength of the author's position.

Mitigation: Have the author review the final response for scientific accuracy, scope, and preservation of the intended position.

## Reference(s):

- [Polite Expressions Library](references/polite_expressions.json)
- [Tone Transformation Patterns](references/tone_patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Plain text or JSON containing a polished response, tone scores, improvements, and suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports reviewer comment, draft response, response type, polish level, and optional file output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
