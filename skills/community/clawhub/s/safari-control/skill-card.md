## Description:

Use Safari directly on macOS when work must happen in the user's real Safari session instead of a separate automation browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gordonynh](https://clawhub.ai/user/gordonynh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and operate the user's real Safari session on macOS when logged-in state, cookies, extensions, open tabs, native Safari controls, or live page content matter. It supports session inspection, DOM reads and actions, native Safari UI automation, waits, screenshots, and page artifact export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and change an authenticated real Safari session, including tabs, page content, form state, native controls, and scripted page behavior.

Mitigation: Use read-only inspection commands before mutating state, scope commands to the intended window or tab, and save the session layout before invasive work when preserving user state matters.

Risk: Saved screenshots, HTML, page bundles, cookies, storage, and form state can contain sensitive account data.

Mitigation: Avoid exports on sensitive sites such as banking, identity, admin, email, password-manager, or production systems unless explicitly needed, and protect or delete exported files after use.

Risk: Enabling Safari automation, JavaScript in the Smart Search field, or JavaScript from Apple Events grants automation more power over the user's real browser session.

Mitigation: Enable these settings intentionally for trusted tasks only, and continue with reduced features or visual desktop control when the user declines.

## Reference(s):

- [Safari Control on ClawHub](https://clawhub.ai/gordonynh/skills/safari-control)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with Swift shell commands, JSON command output, and saved page artifacts such as screenshots, HTML, text, links, tables, snapshots, and page bundles.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS Safari permissions for automation, JavaScript from Apple Events, Accessibility, and screenshot access depending on the command.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
