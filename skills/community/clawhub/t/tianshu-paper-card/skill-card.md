## Description:

Turns a paper abstract or short introduction into a structured Chinese Markdown reading card with placeholders for title, research question, methods, results, limitations, and a citation draft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshengli0421](https://clawhub.ai/user/wangshengli0421)

### License/Terms of Use:

MIT-0

## Use Case:

Students and researchers use this skill to convert pasted abstracts or local abstract files into structured reading notes for literature review, paper summaries, and meeting preparation. The generated citation draft and heuristic sections are intended for review against the original paper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated reading card or citation draft may be inaccurate or incomplete if the abstract is sparse or the heuristic sentence split is wrong.

Mitigation: Review the output against the original paper, especially citations, page references, limitations, and claims.

Risk: The local script reads a file path supplied by the user.

Mitigation: Only pass files that the user intends the script to read.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown reading card printed to stdout, with command-line examples for file or text input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads either user-provided text or a local file path and optionally accepts a title.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
