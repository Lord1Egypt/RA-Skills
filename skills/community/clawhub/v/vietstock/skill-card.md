## Description:

Automated Vietnamese stock price and index checking on FireAnt.vn for stock symbols and market indices, returning formatted price, trading, and financial metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aholake](https://clawhub.ai/user/aholake)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to look up current Vietnamese stock and market index information from FireAnt.vn for symbols such as DPM, VCB, FPT, VNINDEX, HNX30, and VN30.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scraped market information may be incomplete, stale, or affected by external page changes.

Mitigation: Treat outputs as informational and verify important financial data against an authoritative market source before using it for decisions.

Risk: The skill runs a local Python script that opens an OpenClaw-controlled browser and visits Google and FireAnt.

Mitigation: Install and invoke it only in environments where this browser automation is acceptable, and use explicit Vietnamese stock symbols or supported index names.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aholake/skills/vietstock)
- [FireAnt stock and index page pattern](https://fireant.vn/ma-chung-khoan/{SYMBOL})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown-formatted text with stock or index metrics and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from browser-scraped Google and FireAnt pages and may be incomplete or stale.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
