## Description:

RxnIM helps agents parse chemical reaction images into structured reaction data, including SMILES structures, reaction conditions, species roles, and formatted Markdown summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fqiangliu](https://clawhub.ai/user/fqiangliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and chemistry-focused agents use this skill to extract reaction structures and conditions from uploaded or referenced chemical reaction images. It can call a hosted HuggingFace Space or guide local deployment for reaction image parsing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted use sends reaction images to a third-party HuggingFace Space.

Mitigation: Use the hosted path only for data approved for that service; avoid unpublished, proprietary, regulated, or confidential chemistry data unless approval is in place.

Risk: Local deployment instructions include unpinned external repository, dependency, model archive, and script execution steps.

Mitigation: Pin and review the repository, dependencies, model archive, and eval script, then run local deployment in an isolated environment without unnecessary credentials or sensitive mounts.

## Reference(s):

- [RxnIM ClawHub Skill Page](https://clawhub.ai/fqiangliu/skills/rxn-im)
- [RxnIM HuggingFace Space](https://huggingface.co/spaces/CYF200127/RxnIM)
- [RxnIM Model Weights Dataset](https://huggingface.co/datasets/CYF200127/RxnIM)
- [RxnIM Source Repository](https://github.com/CYF2000127/RxnIM)
- [Towards large-scale chemical reaction image parsing via a multimodal large language model](http://dx.doi.org/10.1039/D5SC04173B)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples, Python snippets, shell commands, and structured reaction summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted SMILES strings, reaction conditions, species roles, and full reaction strings from image parsing results.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
