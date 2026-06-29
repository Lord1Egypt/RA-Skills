## Description: <br>
Deterministic rainfall and climate formatting for SWMM that converts rainfall inputs into SWMM-ready TIMESERIES lines, RAINGAGES snippets, and audit JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhonghao1995](https://clawhub.ai/user/zhonghao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and civil or stormwater engineers use this skill to prepare rainfall time series, raingage helper sections, and design-storm inputs for SWMM workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled scripts write to user-selected output paths and may create directories or overwrite files. <br>
Mitigation: Review output paths before execution and run the skill in a controlled project workspace. <br>
Risk: The skill documentation mentions an MCP wrapper, but the server evidence says that wrapper is not included in this artifact version. <br>
Mitigation: Use the bundled command-line scripts directly unless a separately reviewed MCP wrapper is available. <br>


## Reference(s): <br>
- [Agentic SWMM Workflow](https://github.com/Zhonghao1995/agentic-swmm-workflow) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhonghao1995/swmm-climate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated text and JSON file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SWMM TIMESERIES text, RAINGAGES text snippets, and JSON summaries from user-provided rainfall inputs.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
