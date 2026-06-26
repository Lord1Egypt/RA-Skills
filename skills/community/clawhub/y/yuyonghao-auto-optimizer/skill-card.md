## Description: <br>
Auto Optimizer monitors OpenClaw skill performance, analyzes bottlenecks, generates optimization recommendations, and can apply optimization changes to local skill code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use Auto Optimizer to collect performance metrics, identify slow or unstable skill behavior, produce optimization reports, and optionally apply code changes for common performance and reliability issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may edit local skill source files and persist backups or metrics without clear confirmation or path limits. <br>
Mitigation: Use it only on a test copy or version-controlled workspace, restrict target paths yourself, and review proposed or applied changes before deployment. <br>
Risk: Dry-run and rollback behavior may not provide reliable recovery for modified source files. <br>
Mitigation: Do not rely on dry-run or rollback behavior unless you verify it in the code first; keep independent backups before applying optimizations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/yuyonghao-auto-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [JavaScript objects and Markdown optimization reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local metrics and backups, and may modify local skill source files when optimization application is enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
