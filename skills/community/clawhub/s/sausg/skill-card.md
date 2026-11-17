## Description:

SAUSG（结构通用分析与设计软件）自动计算与操作工具。用于弹塑性计算、非线性分析、动力时程分析、隔震减震设计、钢结构分析等。当用户提及 SAUSG、SAUSAGE、OpenSAUSG、SAUSGDelta、SAUSGJG、SAUSGPI、SAUSGZeta 等相关软件，或要求进行弹塑性计算、读取计算结果时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiasu1017-beep](https://clawhub.ai/user/jiasu1017-beep)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and structural engineering users use this skill to open SAUSG models, run sequential structural analysis calculations, and read key calculation outputs from local SAUSG result files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch local SAUSG executables from installation paths.

Mitigation: Use only trusted SAUSG installations and prefer explicitly passing the expected SAUSG directory.

Risk: Default calculation cleanup can delete broad sets of existing SAUSG project result files.

Mitigation: Use --no-cleanup when preserving prior outputs matters, and keep backups or verify the directory contains only disposable SAUSG artifacts before cleanup.

## Reference(s):

- [SAUSG product page](https://product.pkpm.cn/productDetails?productId=56)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and structured result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch local SAUSG executables and may summarize structural calculation results from local files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
