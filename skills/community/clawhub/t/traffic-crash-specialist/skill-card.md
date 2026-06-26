## Description: <br>
Guides agents through traffic crash video analysis resources, including CrashChat and Traffix VideoQA for crash recognition, reasoning, localization, dataset selection, and model training or evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sxy799](https://clawhub.ai/user/sxy799) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and researchers use this skill to identify traffic-crash video analysis models, datasets, and task definitions, then draft installation, training, and evaluation steps for CrashChat and Traffix VideoQA workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Referenced repositories, dependencies, and binary wheels may introduce supply-chain risk if run without review. <br>
Mitigation: Review the CrashChat repository, requirements, and any binary wheel before executing installation or training commands. <br>
Risk: Model and dataset setup may require large downloads and local compute resources. <br>
Mitigation: Confirm storage, bandwidth, GPU, and runtime requirements before starting downloads, training, or evaluation. <br>
Risk: Real traffic or crash footage can carry privacy, consent, licensing, or policy obligations. <br>
Mitigation: Verify dataset terms and organizational privacy requirements before processing or sharing real-world video. <br>


## Reference(s): <br>
- [CrashChat paper](https://arxiv.org/abs/2512.18878) <br>
- [CrashChat GitHub repository](https://github.com/Liangkd/CrashChat) <br>
- [CrashChat Hugging Face model](https://huggingface.co/KDliang/crashchat) <br>
- [CrashChat Hugging Face dataset](https://huggingface.co/datasets/KDliang/CrashChat) <br>
- [Traffix VideoQA project](https://traffix-videoqa.github.io/) <br>
- [Models - 模型架构详解](references/models.md) <br>
- [Datasets - 数据集详解](references/datasets.md) <br>
- [Tasks - 六大任务详解](references/tasks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference external model, dataset, paper, and repository links.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
