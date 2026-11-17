## Description:

Biomolecular structure prediction tools for Chai-1, Boltz-2, and AlphaFold3 via SciMiner APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to invoke SciMiner-hosted Chai-1, Boltz-2, and AlphaFold3 workflows for protein, nucleic acid, ligand, and mixed-complex structure prediction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to build and run API invocation code from mutable remote SciMiner Markdown documentation.

Mitigation: Review the selected SciMiner documentation before execution and confirm destination endpoints, parameters, upload fields, and authentication headers before sending requests.

Risk: The skill uses a SciMiner API key and may upload sensitive biomolecular inputs to SciMiner services.

Mitigation: Store the API key only in the configured credentials file, avoid printing or persisting secrets, and confirm that uploaded biomolecular inputs are approved for SciMiner processing.

## Reference(s):

- [SciMiner API Documentation](https://sciminer.tech/tool_api_files/)
- [SciMiner API Key Utility](https://sciminer.tech/utility)
- [ClawHub Skill Page](https://clawhub.ai/sciminer/skills/structure-prediction)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline JSON, code, shell commands, and SciMiner share URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task_id and share_url values for completed or long-running SciMiner API tasks.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
