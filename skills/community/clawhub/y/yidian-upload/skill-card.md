## Description:

Yidian Upload automates batch product uploads and management for Xianyu shops through the Yidian backend, using Playwright/CDP browser automation with stepwise confirmation and screenshot validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuhao1443796193-commits](https://clawhub.ai/user/yuhao1443796193-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Xianyu sellers and operators use this skill to prepare product listings, publish batches through the Yidian backend, configure auto-delivery links, and optionally synchronize listing status with Feishu spreadsheets. It is intended for logged-in shop workflows where a human can verify account, shop, product data, and dry-run results before live publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a logged-in seller backend and make live listing or shop-management changes.

Mitigation: Use dry-run first, verify the active browser account and target shop, and keep a human review step before live runs.

Risk: The artifact includes a Feishu spreadsheet token and can update external spreadsheet status records.

Mitigation: Rotate or remove embedded Feishu credentials, use least-privilege access, and confirm the target spreadsheet before enabling synchronization.

Risk: Using a general browser profile for CDP automation can expose unrelated sessions or accounts to agent control.

Mitigation: Run CDP automation with a dedicated browser profile that is logged in only to the required seller backend.

Risk: Untrusted product data may be interpolated into browser-side JavaScript or file paths.

Mitigation: Use trusted product inputs only until JavaScript interpolation and filename handling are hardened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuhao1443796193-commits/skills/yidian-upload)
- [Yidian backend](https://ed.weeeg.com)
- [Lark CLI](https://github.com/larksuite/cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and shell commands; scripts produce console logs, local text records, and Feishu status updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run preview paths and sequential browser automation for listing, auto-delivery, and shop-management actions.]

## Skill Version(s):

3.4.0 (source: server release evidence; artifact frontmatter reports 3.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
