## Description:

Use PTS (Pivotal Token Search) to find the tokens, sentences and latent concepts that change whether a language model solves a task, read the resulting events file, explore it in the visualizer, and export it as datasets. Use when the user wants to analyze reasoning steps of a small local model, interpret a PTS events file, or plan a search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sandeep85das](https://clawhub.ai/user/sandeep85das)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to plan local PTS searches, interpret token, sentence, or latent-event results, explore events, and export datasets while managing downloads, compute costs, and sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model or dataset downloads may use substantial storage, bandwidth, or compute.

Mitigation: Ask before downloading and agree on the model, dataset, and computing budget before starting searches.

Risk: Event files may contain sensitive task or model-analysis data.

Mitigation: Keep event files local unless the user explicitly chooses to share or publish them.

Risk: Sampling noise and task-dependent scoring can make apparent effects misleading.

Mitigation: Treat findings as observational, use controls and repeat runs, and avoid causal claims without intervention.

## Reference(s):

- [PTS project](https://github.com/codelion/pts)
- [ClawHub skill release](https://clawhub.ai/sandeep85das/skills/pts-pivotal-token-search)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSONL datasets]

**Output Format:** [Markdown guidance with inline shell commands; PTS event and dataset outputs may be JSONL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results depend on the selected model, task, and sampling settings; observational results do not establish causation.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
