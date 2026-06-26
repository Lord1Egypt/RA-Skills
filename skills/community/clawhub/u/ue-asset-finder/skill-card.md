## Description: <br>
Find Unreal Engine assets such as .uasset, .umap, .uby, and .udata files by asset type, name pattern, or project path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentwilliam](https://clawhub.ai/user/vincentwilliam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical artists use this skill to locate Unreal Engine project assets, maps, UI widgets, blueprints, audio files, data tables, and optional asset reference information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recursive searches that include Saved folders may expose logs, configuration files, or saved-game data from the selected Unreal Engine project. <br>
Mitigation: Review generated search commands before execution and scope searches to Content folders unless Saved data is explicitly required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vincentwilliam/ue-asset-finder) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with PowerShell command snippets and asset metadata summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When assets are found, responses should include full path, file size, last modified date, and dependencies when reference checks are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
