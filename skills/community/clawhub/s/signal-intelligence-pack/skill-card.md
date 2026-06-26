## Description: <br>
A grounding workflow that turns research questions into planned searches, routed sources, cleaned evidence, freshness labels, and counter-evidence before downstream analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z1one0415](https://clawhub.ai/user/z1one0415) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Research agents, analysts, and strategy workflows use this skill to prepare an enhanced evidence base before analysis. It is most useful for external-information tasks that need multi-source grounding, freshness review, or counter-evidence checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts may contain sensitive information that could be passed to available search providers or child skills. <br>
Mitigation: Remove secrets and proprietary details before use, and review which providers and child skills are available in the agent environment. <br>
Risk: The workflow may run additional searches and consume provider quota. <br>
Mitigation: Constrain available sources and time windows when needed, and review search counts, degradation logs, and pending actions in the output. <br>
Risk: The enhanced evidence base can still be incomplete, stale, or affected by source coverage gaps. <br>
Mitigation: Use the freshness labels, counter-evidence results, confidence assessment, and pending actions as review gates before relying on downstream analysis. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/z1one0415/signal-intelligence-pack) <br>
- [Workflow](references/workflow.md) <br>
- [Input/Output Schema](references/input-output.md) <br>
- [Stop Rules](references/stop-rules.md) <br>
- [Examples](references/examples.md) <br>
- [Improvement Plan V2](references/improvement-plan-v2.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [Enhanced evidence base JSON with pipeline metadata, cleaned evidence, freshness labels, counter-evidence, and confidence assessment.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May stop after evidence cleaning or freshness judging for lower-risk tasks; strategic and high-risk tasks run all five steps.] <br>

## Skill Version(s): <br>
2.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
