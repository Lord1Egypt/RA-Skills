## Description:

Traffic Crash Specialist helps agents analyze traffic accident videos, answer traffic-scene video questions, locate crash timing, summarize crash events, reason about causes and prevention, and guide CrashChat or Traffix VideoQA model training and evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxy799](https://clawhub.ai/user/sxy799)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and traffic-analysis teams use this skill to navigate traffic-crash video analysis resources, choose CrashChat or Traffix VideoQA tasks, and generate guidance for setup, evaluation, crash recognition, localization, description, causal reasoning, and prevention reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance may run mutable third-party repository code or model artifacts without pinned revisions or integrity checks.

Mitigation: Install in an isolated environment, pin the CrashChat repository and Hugging Face artifacts to reviewed revisions, verify dependency and wheel checksums, and review shell and Python scripts before running training or evaluation.

Risk: Traffic-crash analysis outputs can be incomplete or incorrect when used for safety, legal, insurance, or operational decisions.

Mitigation: Use outputs as decision-support guidance only and require qualified human review before applying conclusions outside analysis or development workflows.

## Reference(s):

- [CrashChat GitHub Repository](https://github.com/Liangkd/CrashChat)
- [CrashChat Paper](https://arxiv.org/abs/2512.18878)
- [CrashChat Model Weights](https://huggingface.co/KDliang/crashchat)
- [CrashChat Dataset](https://huggingface.co/datasets/KDliang/CrashChat)
- [Traffix VideoQA](https://traffix-videoqa.github.io/)
- [Datasets - 数据集详解](references/datasets.md)
- [Models - 模型架构详解](references/models.md)
- [Tasks - 六大任务详解](references/tasks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model, dataset, task, training, and evaluation guidance for traffic-crash video analysis workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
