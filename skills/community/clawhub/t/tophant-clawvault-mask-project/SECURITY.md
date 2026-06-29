# Security Model

`tophant-clawvault-mask-project` is a lightweight local masking skill for preparing project documents before AI analysis.

## Permissions

- Reads only the input file path provided by the user.
- Writes only when the user provides an output path or asks to save a policy file.
- Does not request network access, credentials, service control, proxy control, or dashboard control.

## Privacy Guarantees

- Applies local masking rules in-process.
- Replaces matched sensitive values with numbered placeholders such as `[mask_1]` and `[mask_2]`.
- Numbered placeholders are for readability only and do not create a restore mapping.
- Can return sanitized content as JSON or write sanitized content to a separate output file.
- Does not modify the original input file.
- Does not create restore mappings.
- Does not log, print, or return raw matched values.

## What This Skill Does Not Do

- Does not start or require the ClawVault proxy.
- Does not start or require the ClawVault dashboard.
- Does not inspect API traffic.
- Does not call external services or send document content over the network.
- Does not provide a hard file-read sandbox; it is a cooperative tool that should be run only on user-approved files.

## Limitations

- Masking is regex-based and can miss sensitive content.
- A no-match result does not guarantee that the file is safe.
- Users should review sanitized output before sharing it with an AI model.
