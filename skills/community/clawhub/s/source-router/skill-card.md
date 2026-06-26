## Description: <br>
Source Router creates a structured search-routing plan that tells an agent which available sources to consult, in what order, whether to include counter-evidence search, when to stop, and how to allocate search budget. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z1one0415](https://clawhub.ai/user/z1one0415) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to decide where to search first across web, local files, vector stores, graph sources, and counter-evidence sources. It is intended for planning search strategy, not for executing searches or producing final conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plan may route an agent to web providers, local folders, memories, caches, vector stores, or graph sources that the user did not intend to query. <br>
Mitigation: Review the available_sources list before using the plan and exclude any sources that should remain out of scope. <br>
Risk: The skill produces routing plans only; treating the plan as evidence or as a final conclusion can mislead downstream work. <br>
Mitigation: Use the output to guide search, then review the retrieved sources before making claims or decisions. <br>


## Reference(s): <br>
- [Source Selection Rules](artifact/references/source-selection-rules.md) <br>
- [Source Router Examples](artifact/references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/z1one0415/source-router) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with structured JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a search-routing plan with selected sources, search order, counter-search setting, stop rule, budget allocation, fallback chain, and degradation log fields.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
