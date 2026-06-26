## Description: <br>
Biomolecular structure prediction tools for Chai-1, Boltz-2, and AlphaFold3 via SciMiner APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to submit biomolecular structure prediction jobs for proteins, DNA, RNA, ligands, and mixed complexes through SciMiner-hosted Chai-1, Boltz-2, and AlphaFold3 APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local SciMiner API key and sends authenticated requests to an external service. <br>
Mitigation: Use a dedicated SciMiner credential stored only at the documented credential path, do not expose it in prompts or logs, and install the skill only when SciMiner is trusted. <br>
Risk: Biomolecular inputs and uploaded files are sent to SciMiner for processing. <br>
Mitigation: Start with non-sensitive test data and avoid proprietary sequences, ligands, structures, or other confidential inputs unless the external-service risk is acceptable. <br>
Risk: The skill relies on live SciMiner Markdown documentation to determine API payloads and invocation behavior. <br>
Mitigation: Review the selected SciMiner API documentation before execution and confirm provider names, tool names, required parameters, upload behavior, and polling flow match the intended task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sciminer/structure-prediction) <br>
- [SciMiner Tool API Files](https://sciminer.tech/tool_api_files/) <br>
- [Chai-1 API Documentation](https://sciminer.tech/tool_api_files/Chai-1_api_doc.md) <br>
- [Boltz-2 API Documentation](https://sciminer.tech/tool_api_files/Boltz-2_api_doc.md) <br>
- [AlphaFold3 API Documentation](https://sciminer.tech/tool_api_files/AlphaFold3_api_doc.md) <br>
- [SciMiner API Key Utility](https://sciminer.tech/utility) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JSON and inline code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task status, task identifiers, and SciMiner share URLs for successful or long-running prediction jobs.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
