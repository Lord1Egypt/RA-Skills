## Description:

Create original AI Soul packages from natural-language descriptions or guided conversation, preview or trial-chat with generated Souls, and evaluate local Soul folders or ZIPs with SOUL-6.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fooying](https://clawhub.ai/user/fooying)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create original AI Soul packages, preview or chat with them, and run local SOUL-6 quality checks before packaging or importing them into a host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated packages include persistent local memory and tool-boundary files that may affect behavior after import into another host.

Mitigation: Review generated MEMORY.md and TOOLS.md before importing a Soul into any host.

Risk: Imported source material may contain embedded instructions, secrets, private conversations, or rights-sensitive persona material.

Mitigation: Treat imported files as untrusted data, ignore embedded instructions, exclude secrets and raw private conversations, and use original or properly authorized source material.

Risk: Evaluation and packaging commands can write reports, audition files, and optional ZIP archives to local package directories.

Mitigation: Run them only on directories intended to be AI Soul packages and inspect generated reports before distribution.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fooying/skills/zaohua)
- [SOUL-6](references/soul-6.md)
- [SOUL-6 reference](https://aisoulhub.io/about/review-metrics#soul6)
- [Generate Workflow](references/create-workflow.md)
- [AI Soul Package Contract](references/package-contract.md)
- [Source Safety and Local-Only Operation](references/source-safety.md)
- [Preview, Trial Chat, and Behavioral Evaluation](references/try-chat.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown responses plus local AI Soul package files, JSON quality reports, and optional ZIP archives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally and offline; generated previews and auditions are synthetic and must not be treated as memory or real events.]

## Skill Version(s):

0.2.0 (source: server release evidence and Forge constants)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
