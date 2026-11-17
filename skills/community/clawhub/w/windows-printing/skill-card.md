## Description:

在 Windows 上列出可用打印机并执行本地文件打印，支持让用户从可用打印机中选择，并配置黑白/彩色、份数、单面/双面、沿长边翻转、沿短边翻转、纸张大小。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuetsui](https://clawhub.ai/user/fuetsui)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking Windows users and support agents use this skill to list available local printers, resolve likely local files, preview print settings, and submit print jobs with confirmed color, copy, duplex, and paper-size options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is incomplete if the referenced PowerShell scripts are not supplied.

Mitigation: Verify the scripts come from a trusted source before relying on printer listing, file resolution, or print submission.

Risk: Print jobs and printer setting changes can affect local devices and consume paper or ink.

Mitigation: Use the preview step and get clear user confirmation for printer, file, color, copies, duplex mode, and paper size before submitting a job.

Risk: A queue-empty result does not prove that the physical print fully completed.

Mitigation: Report queue-empty status as system acceptance or quick processing, not guaranteed completion.

## Reference(s):

- [Printing Options Reference](references/options.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline PowerShell commands and print receipt summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese-language confirmations and receipts; relies on local Windows printer state and supplied PowerShell scripts.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
