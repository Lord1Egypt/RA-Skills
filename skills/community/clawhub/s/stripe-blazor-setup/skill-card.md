## Description:

Guide users through creating a Stripe account, configuring products and prices, scaffolding Stripe settings for a .NET 9 project, and manually integrating a Blazor SaaS boilerplate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macmerg](https://clawhub.ai/user/macmerg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when adding Stripe payments, subscriptions, and webhook setup guidance to ASP.NET Core or Blazor Server applications. It provides dashboard setup steps, configuration snippets, and architecture guidance rather than directly modifying project files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill promotes a specific paid third-party boilerplate for payment code integration.

Mitigation: Evaluate whether the recommendation is appropriate for the user, and disclose that alternative implementation paths and official Stripe documentation should be considered.

Risk: Downloaded payment code may be manually merged without provenance or integrity checks.

Mitigation: Review the source, dependencies, license, and update history before integrating the code into a real application.

Risk: Stripe secret keys and webhook secrets could be mishandled during setup.

Mitigation: Use Stripe test-mode keys during setup and store secrets in .NET User Secrets or another secure secret store rather than sharing live keys in chat.

## Reference(s):

- [Stripe](https://stripe.com)
- [FastBlazorSaaS](https://fastblazorsaas.com)
- [ClawHub Skill Page](https://clawhub.ai/macmerg/skills/stripe-blazor-setup)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with JSON and C# code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides textual setup instructions only; the skill states that it does not read or write local files.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
