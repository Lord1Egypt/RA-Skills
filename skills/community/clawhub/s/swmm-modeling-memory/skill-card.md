## Description: <br>
Read historical Agentic SWMM experiment audit artifacts and summarize repeated assumptions, QA issues, failures, missing evidence, run-to-run differences, lessons learned, and controlled skill update proposals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhonghao1995](https://clawhub.ai/user/zhonghao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill after SWMM experiment audits to summarize historical run evidence, identify repeated QA and failure patterns, and draft human-reviewed skill refinement proposals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has under-scoped filesystem write behavior and may write or overwrite memory summaries in selected output, audited run, or optional Obsidian directories. <br>
Mitigation: Run it first on a copied test directory, set output paths explicitly, avoid broad or symlink-heavy run directories, and review generated summary files before relying on them. <br>
Risk: Generated skill update proposals could carry forward incorrect assumptions or misleading lessons from incomplete audit artifacts. <br>
Mitigation: Treat proposals as review material only and accept refinements only after human review and benchmark verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhonghao1995/swmm-modeling-memory) <br>
- [Agentic SWMM project](https://github.com/Zhonghao1995/agentic-swmm-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON and Markdown files, with shell command examples for running the summarizer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes aggregate memory outputs under the chosen output directory, writes per-run memory_summary.json by default, and can optionally copy Markdown exports to an Obsidian directory.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
