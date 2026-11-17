## Description:

Control Samsung TVs via SmartThings (OAuth app + device control).

This skill is ready for commercial/non-commercial use.

## Publisher:

[regenrek](https://clawhub.ai/user/regenrek)

### License/Terms of Use:


## Use Case:

External developers and smart home users use this skill to configure SmartThings OAuth credentials and guide Samsung TV control through SmartThings device commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad SmartThings read and execute authority can allow control of connected devices until credentials are revoked.

Mitigation: Create the narrowest SmartThings PAT and OAuth permissions available, and revoke or remove credentials when they are no longer needed.

Risk: The default OAuth redirect URI uses a public request-inspection service, which can expose an authorization code.

Mitigation: Use a redirect URI you control before exchanging OAuth codes.

Risk: Generated SmartThings credentials and OAuth tokens are stored in a local .env file.

Mitigation: Treat the .env file as a secret, restrict access to it, and avoid sharing logs or files that include token values.

Risk: The setup script can fall back to running the SmartThings CLI through npx.

Mitigation: Use the npx fallback only when you trust the package source and version, or install a reviewed SmartThings CLI directly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/regenrek/skills/samsung-smartthings)
- [SmartThings Developer Documentation](https://developer.smartthings.com/docs)
- [SmartThings Personal Access Tokens](https://account.smartthings.com/tokens)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain-text setup and device-control guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The setup flow can create or update a local .env file with SmartThings app credentials, OAuth tokens, scopes, and device identifiers.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
