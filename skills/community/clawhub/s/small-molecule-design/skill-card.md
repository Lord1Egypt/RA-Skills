## Description: <br>
Small-molecule generation workflows combining REINVENT4, PocketXMol, fpocket, and Gnina Score through SciMiner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, computational chemists, and research teams use this skill to generate, optimize, and validate small molecules through SciMiner workflows for structure-free design, pocket-guided design, pocket detection, and receptor-based scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a SciMiner API key file. <br>
Mitigation: Store only the SciMiner API key in the configured credentials file and do not print, persist, or copy the key into prompts, logs, or repository files. <br>
Risk: The workflow may upload molecular or protein input files to an external SciMiner service. <br>
Mitigation: Review SciMiner's handling of uploaded scientific data before using confidential, regulated, or proprietary inputs. <br>


## Reference(s): <br>
- [Small molecule design ClawHub page](https://clawhub.ai/sciminer/small-molecule-design) <br>
- [SciMiner tool API documentation](https://sciminer.tech/tool_api_files/) <br>
- [SciMiner API key utility](https://sciminer.tech/utility) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, API calls, JSON] <br>
**Output Format:** [Markdown summaries with API request guidance, JSON result references, task IDs, and share URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SciMiner API key file and may upload user-provided molecular or protein input files to SciMiner.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
