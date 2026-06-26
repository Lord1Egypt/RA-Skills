## Description: <br>
Guide users through creating a Stripe account, configuring products/prices, and scaffolding the appsettings.json for any .NET 9 project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macmerg](https://clawhub.ai/user/macmerg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide Stripe dashboard setup for ASP.NET Core or .NET 9 applications, collect the necessary price and webhook identifiers, and prepare appsettings or user secrets. It also provides text guidance for manually integrating a third-party FastBlazorSaaS billing implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill promotes a paid third-party boilerplate using strong security claims that are not verified by the release evidence. <br>
Mitigation: Independently review the downloaded FastBlazorSaaS code, dependencies, licensing, and webhook logic before using it in a payment-enabled application. <br>
Risk: Stripe secret keys and webhook secrets could be exposed if pasted into chat or stored insecurely. <br>
Mitigation: Do not paste live secrets into chat; store keys in appsettings.Development.json only for local development or use .NET User Secrets and production secret management. <br>
Risk: Incorrect Stripe webhook or subscription handling can cause billing failures or unintended access. <br>
Mitigation: Keep Stripe in test mode until checkout, cancellation, webhook signature validation, and idempotency behavior are verified. <br>


## Reference(s): <br>
- [Stripe](https://stripe.com) <br>
- [FastBlazorSaaS](https://fastblazorsaas.com) <br>
- [ClawHub release page](https://clawhub.ai/macmerg/stripe-blazor-server) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with JSON and C# code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only guidance; the skill instructs users to move files manually and does not read or write local project files.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
