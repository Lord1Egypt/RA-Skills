## Description:

Set up Cloudflare Turnstile end-to-end in a project: scan the codebase, create the widget via the Cloudflare API, deploy the managed siteverify Worker, write the frontend snippets, validate, and persist the skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[creativerezz](https://clawhub.ai/user/creativerezz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Cloudflare Turnstile bot protection to signup, login, contact, or similar forms. It guides account authentication, widget creation, managed Worker deployment, frontend integration, validation, and optional skill persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests Cloudflare permissions that can create Turnstile widgets and deploy Workers in an account.

Mitigation: Review the scripts before installation, use a short-lived account-scoped token, and confirm each account mutation before running it.

Risk: Remote install or deploy steps can depend on mutable upstream content.

Mitigation: Prefer the bundled Worker template, and only run the persistence step when the source is pinned or otherwise verified.

Risk: Cloudflare API tokens or Turnstile secrets may be exposed if pasted into chat or captured in logs.

Mitigation: Avoid pasting credentials into chat, pass secrets through environment variables or secure files, and rotate any token or secret that appears in logs.

## Reference(s):

- [Turnstile Spin docs](https://developers.cloudflare.com/turnstile/spin/)
- [Cloudflare Turnstile docs](https://developers.cloudflare.com/turnstile/)
- [Server-side validation reference](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/)
- [cloudflare/turnstile-siteverify](https://github.com/cloudflare/turnstile-siteverify)
- [cloudflare/skills](https://github.com/cloudflare/skills)
- [Pages Plugin for Turnstile](https://developers.cloudflare.com/pages/functions/plugins/turnstile/)
- [reCAPTCHA migration guide](https://developers.cloudflare.com/turnstile/migration/recaptcha/)
- [Vanilla HTML reference](references/vanilla-html.md)
- [Next.js App Router reference](references/nextjs-app.md)
- [Next.js Pages Router reference](references/nextjs-pages.md)
- [Astro reference](references/astro.md)
- [SvelteKit reference](references/sveltekit.md)
- [Hugo reference](references/hugo.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, JSON script outputs, and file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Cloudflare Turnstile widgets, deploy a managed Cloudflare Worker, update project source files, and persist the skill bundle after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
