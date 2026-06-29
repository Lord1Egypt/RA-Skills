## Description: <br>
Top-level orchestration skill for agentic SWMM modelling. Use when an agent needs one entrypoint that decides which module tools to run, in what order, and when to stop, for example to build, run, QA, and optionally calibrate a SWMM case from prepared or partially prepared inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhonghao1995](https://clawhub.ai/user/zhonghao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and stormwater modelers use this skill to coordinate end-to-end SWMM modeling workflows, including build, run, QA, audit, and optional calibration or uncertainty steps from prepared or partially prepared inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can run local project tooling and dependency installation steps. <br>
Mitigation: Install and run it only from the intended Agentic SWMM repository, and review dependency installation before MCP setup. <br>
Risk: Audit notes or raw MCP responses can contain project paths, model metadata, or other sensitive case details. <br>
Mitigation: Treat generated run artifacts as sensitive and use --no-obsidian when audit notes should stay only under runs/<case>. <br>
Risk: The skill may write audit notes outside the run folder unless disabled. <br>
Mitigation: Disable Obsidian export with --no-obsidian when external note export is not intended. <br>


## Reference(s): <br>
- [Agentic SWMM project](https://github.com/Zhonghao1995/agentic-swmm-workflow) <br>
- [ClawHub skill page](https://clawhub.ai/zhonghao1995/swmm-end-to-end) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, MCP tool names, JSON artifact contracts, and run-local file path conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates existing Agentic SWMM MCP tools and scripts; outputs may include run manifests, raw MCP responses, audit notes, QA metrics, plots, and SWMM model artifacts.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
