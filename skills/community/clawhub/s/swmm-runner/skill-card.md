## Description: <br>
Run EPA SWMM simulations through swmm5, create reproducible run artifacts, and extract peak-flow, continuity, and comparison metrics from SWMM report files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhonghao1995](https://clawhub.ai/user/zhonghao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill after a SWMM input model is assembled to run the local solver, collect standard output files, and read hydrology metrics from SWMM report output. It is also useful for comparing report files across runs, such as CLI versus GUI parity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes solver artifacts into the selected run directory and may overwrite same-named files. <br>
Mitigation: Use a dedicated run directory for each simulation and avoid sensitive, shared, or project-root paths. <br>
Risk: Runs depend on the local swmm5 executable and environment configuration. <br>
Mitigation: Verify the intended swmm5 binary and version before running, especially when using PATH, AISWMM_SWMM5, or AISWMM_CONFIG_DIR. <br>


## Reference(s): <br>
- [Agentic SWMM project](https://github.com/Zhonghao1995/agentic-swmm-workflow) <br>
- [ClawHub skill page](https://clawhub.ai/zhonghao1995/swmm-runner) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus JSON manifests and SWMM output files produced by the toolchain] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces run directories containing rpt, out, stdout, stderr, and manifest.json; parser commands return structured JSON metrics.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
