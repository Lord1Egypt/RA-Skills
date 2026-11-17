## Description:

Extract metadata from Xiaohongshu (XHS) share or discovery URLs by parsing window.__INITIAL_STATE__ and returning note details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jovijovi](https://clawhub.ai/user/jovijovi)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agents use this skill to fetch public Xiaohongshu note metadata, engagement counts, tags, user details, and video stream information for summarization or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The extractor accepts arbitrary URLs and follows redirects, which may let it reach localhost, private networks, cloud metadata endpoints, or sensitive internal systems.

Mitigation: Run it only on trusted public Xiaohongshu URLs, and add domain, IP, redirect, and output-path validation before broader use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, files]

**Output Format:** [JSON written to stdout or a file, with optional flattened records and JSON error payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports pretty printing, flat-only output, output-file writing, configurable timeout, and JSON-formatted errors.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-02-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
