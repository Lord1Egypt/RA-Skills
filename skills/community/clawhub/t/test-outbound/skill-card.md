## Description:

Logs in to the outbound workbench and saves a reusable browser session as auth.json for first-time login, expired sessions, or task setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ringorangers](https://clawhub.ai/user/ringorangers)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and developers use this skill to prepare or refresh authenticated browser state before outbound workbench tasks. It guides credential-file setup, Playwright/Chromium prerequisites, manual captcha completion, and session reuse through auth.json.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: login_credentials.json and auth.json may expose account credentials or reusable authenticated session state if committed, backed up, or shared.

Mitigation: Use the skill only in a protected workspace, keep both files out of source control and backups, restrict file permissions, and revoke or rotate the account/session if either file may have been exposed.

Risk: A stale or invalid auth.json can make downstream outbound tasks operate without a valid authenticated session.

Mitigation: Recheck the saved session after login by loading auth.json in a fresh browser context and confirming the outbound workbench opens successfully before reuse.

Risk: Unpinned browser automation dependencies can change login behavior or introduce avoidable supply-chain risk.

Mitigation: Run Playwright and Chromium in an isolated environment and prefer pinned Playwright versions.

## Reference(s):

- [Session Contract](references/session-contract.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and an auth.json browser-session file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Playwright, Chromium, local browser access, login_credentials.json, and manual captcha completion.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
