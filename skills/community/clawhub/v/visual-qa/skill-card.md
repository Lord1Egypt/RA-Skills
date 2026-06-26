## Description: <br>
Visual regression testing pipeline for web applications. Capture baseline screenshots, compare against new builds using pixel-level diffing, and gate deployments based on visual similarity thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kbo4sho](https://clawhub.ai/user/kbo4sho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to capture baseline screenshots, compare new web application builds against those baselines, and gate merges or deployments with configurable visual similarity thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start a local server command supplied through CLI or config. <br>
Mitigation: Only use trusted server commands and run dependencies in a controlled virtual environment or CI image. <br>
Risk: Captured screenshots and diff images may contain sensitive application data. <br>
Mitigation: Treat .visual-qa screenshots and diffs as sensitive artifacts and manage retention, sharing, and ignores accordingly. <br>
Risk: Replacing approved baselines can hide unintended visual regressions. <br>
Mitigation: Review baseline deletion and replacement before accepting updated reference images. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, screenshot files, and diff image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces baseline, current, and diff PNG files; gate.py returns exit code 0 for pass and 1 for fail.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
