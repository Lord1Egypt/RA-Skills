## Description: <br>
SOTA Agent is a public ClawHub SOTA-campaign skill for CV and DS work. Use it when the user says "sota agent", "state of the art benchmark scouting", or wants benchmark planning, paper triage, ablation design, and claim review for CV or data-science campaigns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and review computer-vision or data-science SOTA campaigns with fixed benchmark contracts, paper triage, ablation planning, and claim-safety review. It helps separate planning and evidence review from external execution artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask users to handle credentials or tokens for related campaign work. <br>
Mitigation: Only provide credentials that match the skill's stated purpose and keep execution credentials out of public planning records. <br>
Risk: VirusTotal telemetry was pending in the available security evidence. <br>
Mitigation: Treat the scan as incomplete telemetry and review requested permissions before installation. <br>
Risk: Benchmark planning can produce misleading SOTA claims if metric, split, baseline, or evidence standards drift. <br>
Mitigation: Freeze the benchmark contract, require reproduced baselines, and use the bundled claim-safety review before promotion. <br>


## Reference(s): <br>
- [SOTA Agent homepage](https://zack-dev-cm.github.io/) <br>
- [SOTA Agent ClawHub page](https://clawhub.ai/zack-dev-cm/sota-agent) <br>
- [Benchmark Discipline](references/benchmark-discipline.md) <br>
- [Campaign Harness Stack](references/campaign-harness-stack.md) <br>
- [Claim Safety](references/claim-safety.md) <br>
- [Execution Evidence Summary](references/execution-evidence-summary.md) <br>
- [External Evidence Handoff](references/external-evidence-handoff.md) <br>
- [Paper Triage](references/paper-triage.md) <br>
- [Public Research Lane](references/public-research-lane.md) <br>
- [Public Safety](references/public-safety.md) <br>
- [SOTA Campaign Playbook](references/sota-campaign-playbook.md) <br>
- [SOTA Program Rules](references/sota-program-rules.md) <br>
- [Codex multi-agent guidance](https://developers.openai.com/codex/multi-agent/) <br>
- [Codex customization guidance](https://developers.openai.com/codex/concepts/customization/) <br>
- [Harness engineering](https://openai.com/index/harness-engineering/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON records and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces planning records, review packets, scoreboards, summaries, and redacted evidence references for benchmark campaigns.] <br>

## Skill Version(s): <br>
1.4.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
