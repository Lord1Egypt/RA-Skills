## Description:

Imports user-created notes from Kindle HTML or XHTML notebook exports into a slipbox while skipping highlights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrswab](https://clawhub.ai/user/jrswab)

### License/Terms of Use:


## Use Case:

External users use this skill to import their Kindle reading notes into a slipbox after reviewing the parsed book title, author, and note count. It is intended for Kindle notebook exports where highlights should be excluded and only user-authored notes should become slipbox entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kindle notes may contain private reading notes or personal annotations.

Mitigation: Use the skill only on exports the user intends to process, and ask for confirmation before creating slipbox entries.

Risk: Incorrect parsing could import the wrong number of notes or attach entries to incomplete book metadata.

Mitigation: Display the parsed title, author, and note count as a precheck so the user can review them before import.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with slipbox entry content and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows a precheck with title, author, and note count before creating slipbox entries.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
