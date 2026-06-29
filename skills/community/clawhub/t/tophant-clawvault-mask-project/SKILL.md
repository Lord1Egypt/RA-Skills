---
name: tophant-clawvault-mask-project
version: 0.1.0
description: Mask sensitive company-project document content before analysis
homepage: https://github.com/tophant-ai/ClawVault
user-invocable: true
disable-model-invocation: false
---

# ClawVault Project Document Masking

Use this skill when a user asks to analyze a local company or project document only after ClawVault checks and desensitizes it.

## Example User Request

```text
Please analyze project.txt. It is a company project document, so use @clawvault to check and mask it first.
```

## Required Safety Flow

When the user requests ClawVault masking before analysis:

1. Do not directly read the original file for analysis.
2. Run this skill first against the user-specified file.
3. Analyze only the returned `sanitized_content` or the file written by `--output`.
4. Do not quote, summarize, or expose original sensitive values.
5. Do not restore numbered placeholders such as `[mask_1]` to original values.

This skill masks sensitive business values with numbered non-reversible placeholders such as `[mask_1]`, `[mask_2]`, and `[mask_3]`. It does not create a reversible mapping.

## Commands

### /tophant-clawvault-mask-project generate-policy

Generate the default company-project masking policy.

```bash
/tophant-clawvault-mask-project generate-policy
/tophant-clawvault-mask-project generate-policy --save-policy /tmp/clawvault-policy.json
```

### /tophant-clawvault-mask-project mask-file

Mask a local document and return JSON containing sanitized content.

```bash
/tophant-clawvault-mask-project mask-file project.txt
/tophant-clawvault-mask-project mask-file project.txt --output project.masked.txt
/tophant-clawvault-mask-project mask-file project.txt --policy /tmp/clawvault-policy.json
/tophant-clawvault-mask-project mask-file project.txt --save-policy /tmp/clawvault-policy.json
```

## What Gets Masked

The default policy targets:

- Company names with common Chinese or English organization suffixes.
- Project amount values, especially after labels such as `Project Amount`, `Contract Amount`, `Budget`, `项目金额`, `合同金额`, or `预算`.
- Contextual person names after labels such as `Project Manager`, `Contact`, `Owner`, `负责人`, `联系人`, or `项目经理`.

For label-introduced values, the label is preserved and only the sensitive value is masked.

```text
Project Amount: USD 300,000
```

becomes:

```text
Project Amount: [mask_1]
```

Chinese project-document values are also supported. For example:

```text
客户公司：上海示例科技有限公司
项目金额：人民币三百万元
项目经理：张伟
联系人：李娜
```

becomes:

```text
客户公司：[mask_1]
项目金额：[mask_2]
项目经理：[mask_3]
联系人：[mask_4]
```

## No-Match Warning

If no sensitive content is matched, the skill returns the original content as `sanitized_content`, sets `detections` to `0`, and includes this warning:

```text
No matching sensitive content was found. This does not guarantee the document is safe; it only means the current policy did not match.
```

## Privacy Rules

- Reads only the user-specified input file.
- Never modifies the original file.
- Writes only optional sanitized output files or optional saved policy JSON files.
- Does not request network access.
- Does not start or require the ClawVault proxy or dashboard.
- Does not access credentials.
- Does not output original matched values.
