## Description: <br>
Assemble runnable SWMM INP and manifest artifacts deterministically from subcatchment geometry and attributes, merged parameter JSON, network JSON, and climate references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhonghao1995](https://clawhub.ai/user/zhonghao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers building Agentic SWMM workflows use this skill to assemble auditable SWMM .inp model files and manifests from upstream parameter, network, climate, and subcatchment inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-specified output paths can overwrite existing local files. <br>
Mitigation: Review the INP and manifest output paths before running the builder and prefer a dedicated working directory. <br>
Risk: Generated manifests include source paths and hashes that may reveal local project structure. <br>
Mitigation: Review manifests before sharing them and avoid sensitive directory names or input paths. <br>
Risk: Missing or inconsistent upstream SWMM inputs can produce validation failures or unusable model artifacts. <br>
Mitigation: Use the emitted validation diagnostics and verify subcatchment, parameter, network, climate, and optional water-quality inputs before downstream simulation. <br>


## Reference(s): <br>
- [ClawHub Swmm Builder release](https://clawhub.ai/zhonghao1995/swmm-builder) <br>
- [Agentic SWMM workflow project](https://github.com/Zhonghao1995/agentic-swmm-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands and file paths; generated artifacts are SWMM INP text and manifest JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-specified local inputs and writes user-specified INP and manifest files.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
