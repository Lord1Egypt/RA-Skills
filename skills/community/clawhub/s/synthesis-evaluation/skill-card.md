## Description:

Synthesis evaluation workflows combining SynFormer-ED, Retrosynthesis Planner, and SAScore through SciMiner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and cheminformatics users use this skill to generate synthesizable analogs, evaluate synthetic accessibility, and request retrosynthetic route recommendations through SciMiner workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote documentation can change the request payloads or invocation flow an agent follows.

Mitigation: Review the selected SciMiner documentation before use and prefer a version that pins reviewed endpoints and schemas locally.

Risk: The workflow uses a local SciMiner API key and may process user-provided files.

Mitigation: Store the API key outside the repository, avoid printing or persisting it, and use the skill only when the SciMiner documentation host is trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sciminer/skills/synthesis-evaluation)
- [SciMiner Tool API Files](https://sciminer.tech/tool_api_files/)
- [Synformer API Documentation](https://sciminer.tech/tool_api_files/Synformer_api_doc.md)
- [Retrosynthesis Planner API Documentation](https://sciminer.tech/tool_api_files/Retrosynthesis%20Planner_api_doc.md)
- [SAScore API Documentation](https://sciminer.tech/tool_api_files/SAScore_api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with JSON task results and share URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated API request code, polling guidance, result summaries, and SciMiner share URLs.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
