## Description:

Recognizes six-digit stock codes in stock screenshots with RapidOCR, deduplicates them, keeps a 30-stock FIFO list, and saves entries to manual_stock_list.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wy859](https://clawhub.ai/user/wy859)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert stock screenshots into a maintained local stock-list file for quant workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes stock-list state to a hardcoded local path by default.

Mitigation: Review the target path before use and run with a disposable or backed-up stock-list file until the path is configured for the intended environment.

Risk: The image identifier can cause the OCR script to read unintended JPG files from the inbound media directory.

Mitigation: Validate image identifiers and prefer explicit trusted image paths when processing untrusted inputs.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration]

**Output Format:** [Console text with JSON file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates manual_stock_list.json with deduplicated stock entries and a 30-stock FIFO limit.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
