## Description:

Searches Taobao by product image, compares candidate listings, and can add a selected similar item to the user's cart through a Playwright-backed workflow with browser fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lazygunner](https://clawhub.ai/user/lazygunner)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user provides a product image and asks to find identical or similar Taobao items, compare candidates, or add a chosen item to cart. It is intended for shopping assistance workflows that require user-provided images and an authenticated Taobao session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reusable Taobao login sessions locally, including cookies and storage state that should be treated as account credentials.

Mitigation: Run only on a trusted personal machine or sandbox, avoid uploading or sharing verification-artifacts/taobao-storage-state.json and .pw-user-data-taobao/, and delete those files when finished.

Risk: The workflow can automatically add an item to a live Taobao shopping cart without a strong confirmation gate.

Mitigation: Use the full script only when the user explicitly wants cart modification, and prefer search-only or browser fallback review when the item choice is uncertain.

Risk: The security verdict is suspicious because the skill combines account session persistence with live shopping-cart automation.

Mitigation: Review before installing with a real Taobao account, pin Playwright with a lockfile in sensitive environments, and inspect generated artifacts after each run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lazygunner/skills/taobao-image-search)
- [Publisher Profile](https://clawhub.ai/user/lazygunner)
- [Taobao](https://www.taobao.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, structured JSON result files, execution logs, and screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write verification artifacts including result.json, run-log.txt, screenshots, browser storage state, and a persistent Playwright user data directory.]

## Skill Version(s):

1.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
