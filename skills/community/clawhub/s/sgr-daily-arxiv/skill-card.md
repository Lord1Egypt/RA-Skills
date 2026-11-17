## Description:

Searches arXiv for latest papers by keyword and generates a structured daily report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adaxigua](https://clawhub.ai/user/adaxigua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical readers use this skill to discover recent arXiv computer science papers by keyword and receive a concise Chinese briefing with selected takeaways.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on an arXiv-search helper skill and may not run as intended if that helper is unavailable.

Mitigation: Confirm the helper skill is available before use or adapt the search step to another arXiv retrieval method.

Risk: The default report language is Chinese, which may not fit every user or workflow.

Mitigation: Request another output language explicitly or adjust the skill text before running the workflow.

Risk: The skill selects one top paper per keyword, so relevant papers can be omitted from the final briefing.

Mitigation: Review retrieved candidates when coverage matters and adjust keywords or selection criteria as needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style Chinese briefing with paper titles, links, and five-question analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses keywords supplied by the user or automation prompt and adds one random discovery keyword.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
