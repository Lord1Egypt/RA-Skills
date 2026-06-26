## Description: <br>
Virtual screening workflows for open and proprietary chemical libraries, including transformer-based screening and docking-based screening through SciMiner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and developers use this skill to choose and run SciMiner virtual-screening workflows for open or proprietary chemical libraries against protein targets, then return task results and share links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a SciMiner API key stored at ~/.config/sciminer/credentials.json. <br>
Mitigation: Keep the key outside repositories and prompts, do not print or log it, and use it only as the X-Auth-Token header for SciMiner calls. <br>
Risk: Screening input files may be uploaded to SciMiner. <br>
Mitigation: Do not use confidential chemical libraries or unpublished structures unless SciMiner's terms and the user's data-handling requirements allow it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sciminer/virtual-screening) <br>
- [SciMiner utility and API key page](https://sciminer.simm.ac.cn/utility) <br>
- [SciMiner tool API documentation](https://sciminer.simm.ac.cn/tool_api_files/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with JSON task status, API invocation details, and SciMiner share URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task IDs and share URLs for successful SciMiner jobs.] <br>

## Skill Version(s): <br>
1.0.6 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
