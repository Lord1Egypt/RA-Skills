## Description:

自动扫描 workspace/skills 目录中多种文件，识别风险关键词，生成安全审计报告并给出安装建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tlcyqj2023](https://clawhub.ai/user/tlcyqj2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill reviewers use this skill to run a local heuristic scan of skill files, identify risky code patterns, and receive advisory install or review guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate broadly for common security-review phrases.

Mitigation: Invoke it deliberately and confirm the workspace being reviewed before relying on its output.

Risk: Install-safety recommendations are based on keyword heuristics and can miss or overstate risk.

Mitigation: Treat the report as advisory and manually review skipped, whitelisted, or high-impact files before installation decisions.

Risk: The scanner writes Markdown and JSON reports under /workspace.

Mitigation: Run it only where those output files are expected, or review the configured report paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tlcyqj2023/skills/skill-vetter-2)
- [Publisher profile](https://clawhub.ai/user/tlcyqj2023)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [markdown, json, guidance, shell commands]

**Output Format:** [Markdown report and JSON report, with brief console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports under /workspace when executed; findings are heuristic and advisory.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog; artifact version labels differ)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
