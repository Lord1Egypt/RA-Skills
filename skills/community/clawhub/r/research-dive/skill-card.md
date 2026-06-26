## Description: <br>
Deep web research with multi-round search, cross-verification, and structured reports with citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyatt88](https://clawhub.ai/user/wyatt88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to turn broad research requests into planned web searches, source fetching, cross-checking, and cited research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched webpage content may be incomplete, stale, or untrusted. <br>
Mitigation: Review generated citations and verify important claims against the cited sources before relying on the report. <br>
Risk: The helper runs a local Python script and writes temporary JSON files and Markdown research reports. <br>
Mitigation: Run it in a workspace where generated research files are expected, and review saved outputs before sharing or acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wyatt88/research-dive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, configuration] <br>
**Output Format:** [JSON research plans and fetch instructions, plus Markdown summaries and reports with numbered citations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports quick, standard, and deep modes; reports may be saved under a research directory and include source tiers, confidence notes, and research logs.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
