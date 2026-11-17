## Description:

SOTA Agent is a public ClawHub SOTA-campaign skill for CV and DS work. Use it when the user says "sota agent", "state of the art benchmark scouting", or wants benchmark planning, paper triage, ablation design, and claim review for CV or data-science campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan CV and data-science SOTA campaigns, freeze benchmark contracts, triage papers and leaderboards, design ablations, and review whether execution evidence supports a claim.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated summaries and campaign artifacts may omit or fail to fully scrub sensitive information before publication.

Mitigation: Keep outputs in a dedicated workspace, avoid secrets and private notebook or session data in program and candidate JSON, run the local public-safety checks, and manually review generated Markdown before publishing.

Risk: A benchmark claim can be misleading if the task, metric, split, baseline, or evidence bundle changes during the campaign.

Mitigation: Freeze the benchmark contract before optimization, require reproduced baseline evidence, keep sanitized artifact references, and hold claims that lack repeatable full-surface support.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/skills/sota-agent)
- [Publisher homepage](https://zack-dev-cm.github.io/)
- [SOTA campaign playbook](references/sota-campaign-playbook.md)
- [SOTA program rules](references/sota-program-rules.md)
- [Benchmark discipline](references/benchmark-discipline.md)
- [Paper triage](references/paper-triage.md)
- [Claim safety](references/claim-safety.md)
- [Public safety](references/public-safety.md)
- [External evidence handoff](references/external-evidence-handoff.md)
- [Execution evidence summary](references/execution-evidence-summary.md)
- [Public research lane](references/public-research-lane.md)
- [Campaign harness stack](references/campaign-harness-stack.md)
- [Karpathy autoresearch](https://github.com/karpathy/autoresearch)
- [Codex multi-agent documentation](https://developers.openai.com/codex/multi-agent/)
- [Codex customization documentation](https://developers.openai.com/codex/concepts/customization/)
- [OpenAI harness engineering](https://openai.com/index/harness-engineering/)
- [OpenEvolve](https://github.com/algorithmicsuperintelligence/openevolve)
- [OpenAI Symphony](https://github.com/openai/symphony)
- [Paperclip](https://github.com/paperclipai/paperclip)
- [OptiLLM](https://github.com/algorithmicsuperintelligence/optillm)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, code]

**Output Format:** [Markdown guidance with command examples plus generated JSON and Markdown artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Python helper scripts create campaign records, benchmark snapshots, paper triage queues, candidate cards, scoreboards, review packets, redacted artifact manifests, and concise claim summaries.]

## Skill Version(s):

1.4.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
