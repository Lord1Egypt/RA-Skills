## Description:

Integrates and administers Yandex SmartCaptcha for website widgets, React and Vue SPAs, mobile WebViews, server-side token validation, Yandex Cloud setup, troubleshooting, and pricing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rekryt](https://clawhub.ai/user/rekryt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Yandex SmartCaptcha to web, SPA, and mobile application flows, validate tokens on the backend, manage captcha resources in Yandex Cloud, and troubleshoot integration behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation helpers and examples may use fail-open behavior that weakens login, registration, payment, password reset, or other abuse-sensitive flows if copied unchanged.

Mitigation: Make the failure policy explicit for each protected action and prefer fail-closed behavior for sensitive flows.

Risk: Secret handling, user-submitted output, WebView navigation, dependency pinning, or cloud-resource changes can create production risk if applied without review.

Mitigation: Keep server keys in secret storage or environment variables, escape or return JSON for user-submitted output, restrict WebView origins and navigation, pin dependencies, and require deliberate approval for destructive or broad cloud changes.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/rekryt/skill-smartcaptcha)
- [ClawHub skill page](https://clawhub.ai/rekryt/skills/skill-smartcaptcha)
- [Yandex SmartCaptcha documentation](https://yandex.cloud/ru/docs/smartcaptcha/)
- [Yandex SmartCaptcha quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart)
- [Yandex SmartCaptcha validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation)
- [Yandex SmartCaptcha widget methods](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods)
- [Yandex SmartCaptcha React integration](https://yandex.cloud/ru/docs/smartcaptcha/concepts/react)
- [Yandex SmartCaptcha API reference](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration examples, and file templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include runnable validation helpers and integration templates for web, React, Vue, mobile WebView, and backend services.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
