## Description:

Set up server-side conversion tracking so purchases are reported accurately to Facebook, TikTok, Google and Bing despite iOS restrictions, ad blockers and cookie loss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autonnel](https://clawhub.ai/user/autonnel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and growth engineers use this skill to design and verify server-side conversion reporting for paid traffic funnels across Facebook, TikTok, Google Ads, and Microsoft Bing. It is most useful when browser pixels under-report purchases, attribution identifiers are lost across funnel steps, or ad optimization has degraded after tracking changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run an external Docker deployment that can handle ad platform credentials and customer conversion data without immutable pinning.

Mitigation: Review before installing or following deployment steps, pin the external repository to a reviewed commit, pin container images by digest, and verify signatures or checksums where available.

Risk: Server-side conversion reporting can process hashed customer identifiers and other conversion data subject to consent and privacy requirements.

Mitigation: Only send conversion data when required consent and privacy disclosures are in place, and set production secrets directly in the deployment environment.

Risk: Following deployment steps in a shared or production environment can expose credentials or affect live conversion reporting.

Mitigation: Run the deployment in an isolated environment first and review the configuration before scaling spend or connecting production ad accounts.

## Reference(s):

- [Autonnel repository](https://github.com/autonnel/autonnel)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with tables, checklists, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup sequencing, platform-specific conversion mechanisms, verification checks, and consent-related cautions.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
