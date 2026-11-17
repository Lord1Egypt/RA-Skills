## Description:

Quark Netdisk automates Quark Drive QR login, file browsing and search, uploads, share-link creation with expiry and passcode options, and saving external shared links into a user's drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stnjjjjj](https://clawhub.ai/user/stnjjjjj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate an authenticated Quark Drive account from an OpenClaw agent, including login, allowed-path file management, upload, sharing, and saving external shares.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Quark Drive access can expose account files and account actions to the agent.

Mitigation: Install only where the agent is trusted to operate the account, keep operations scoped to configured local and remote allowlists, and require confirmation for destructive actions.

Risk: Server security evidence reports allowlist protections that can be bypassed.

Mitigation: Fix allowlist checks to use path-aware containment before relying on the skill for sensitive files or broad account access.

Risk: Server security evidence reports account cookies stored without enforced private file permissions.

Mitigation: Store session and cookie files with owner-only permissions and avoid printing cookies, auth headers, QR tokens, or raw authenticated responses.

Risk: Share links may expose user files beyond the intended audience.

Mitigation: Prefer expiring, passcode-protected shares and review the selected file or folder before creating a link.

## Reference(s):

- [Configuration example](references/config.example.json)
- [QuarkPan attribution](https://github.com/lich0821/QuarkPan)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance, shell command examples, JSON status and action payloads, and generated local files such as QR images or session data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses machine-readable exit codes for login, selection, and confirmation flows; runtime session and cookie files are sensitive.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
