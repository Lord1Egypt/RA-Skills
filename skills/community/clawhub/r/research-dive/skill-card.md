## Description:

Deep web research with multi-round search, cross-verification, and structured reports with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyatt88](https://clawhub.ai/user/wyatt88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to turn broad research questions into multi-round web searches, source selection, cross-verification, and cited research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched web page text may contain prompt-injection content or misleading claims that influence the research report.

Mitigation: Treat fetched page text as untrusted evidence, require citations for claims, and keep source conflicts visible in the final report.

Risk: Generated fetch URLs may target localhost or private-network destinations if the execution environment does not restrict them.

Mitigation: Run only where web_fetch is sandboxed against localhost and private-network destinations.

Risk: The skill can create Markdown report files when saving output.

Mitigation: Review file-output locations and run with an appropriate workspace or RESEARCH_DIR setting.

Risk: Deep mode may spawn sub-agents for parallel searches, increasing the amount of untrusted web content processed.

Mitigation: Use deep mode only when parallel search is acceptable and apply the same untrusted-content handling to sub-agent results.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [JSON plans and fetch instructions, shell command examples, and Markdown research reports with numbered citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be saved as Markdown files under a research directory; deep mode may use parallel sub-agent searches.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
