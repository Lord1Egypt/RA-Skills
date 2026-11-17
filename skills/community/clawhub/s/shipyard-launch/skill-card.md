## Description:

Take an app from a free test address to a real product: own domain, real sign-up emails, privacy and terms pages, payments, an email list, phone and desktop apps, and a go-live check. Use for "launch", "go live", "custom domain", "real emails", "privacy policy", "terms", "payments", "Stripe", "subscriptions", "newsletter", "app store", "play store", "publish to the app stores", "Capacitor", "TestFlight", "store screenshots", "desktop app", or "/shipyard:launch". If the folder has no .shipyard-app.json, do not stop: follow the new-app upgrade guide and do the full standard instead of the launch scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipposk](https://clawhub.ai/user/philipposk)

### License/Terms of Use:

MIT-0

## Use Case:

App developers use this skill to prepare an existing application for launch by setting up its domain, sign-up email, legal pages, payments, newsletter, and app store releases. It guides the work and the checks needed before going live.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search setup may redeploy production apps beyond the one selected.

Mitigation: Review the required full plugin, restrict access to the intended app, project, and domain, and require approval before redeploying another project.

Risk: Resetting credentials on an existing account or testing email flows with real user content can affect people or expose personal information.

Mitigation: Confirm an account is a dedicated demo account before resetting credentials, and use synthetic content for email testing.

Risk: Generated privacy and terms text may not meet the app owner's legal or tax obligations.

Mitigation: Treat legal text and country notes as drafts and research, and have them checked before taking real payments.

## Reference(s):

- [Shipyard launch skill on ClawHub](https://clawhub.ai/philipposk/skills/shipyard-launch)
- [Own address and sign-up email guide](references/domain-email.md)
- [Privacy and terms guide](references/legal.md)
- [Payments guide](references/payments.md)
- [Go-live guide](references/go-live.md)
- [App store preparation guide](references/stores.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance, shell commands, and application configuration or source files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some launch steps require the app owner's actions in domain, email, payment, or app store dashboards.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
