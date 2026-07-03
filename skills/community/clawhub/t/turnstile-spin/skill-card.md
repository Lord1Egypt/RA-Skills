## Description: <br>
Set up Cloudflare Turnstile end to end in a project by scanning the codebase, creating a widget, deploying a managed siteverify Worker, wiring frontend snippets, validating the integration, and persisting the skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[creativerezz](https://clawhub.ai/user/creativerezz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Cloudflare Turnstile bot protection to signup, login, contact, or similar forms while keeping existing form behavior intact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Cloudflare API credentials that can create Turnstile resources and deploy Workers. <br>
Mitigation: Use a least-privilege, temporary Cloudflare token and provide it through an environment variable or protected local file rather than chat. <br>
Risk: Turnstile secrets or Cloudflare tokens may be exposed if they are pasted into chat or captured in logs. <br>
Mitigation: Avoid pasting secrets into chat, avoid sensitive values in Turnstile cdata, and rotate any token or Turnstile secret that may have appeared in logs. <br>
Risk: Frontend edits could change form behavior while adding Turnstile validation. <br>
Mitigation: Review diffs before edits and keep the existing submit handler logic gated on Turnstile success rather than replacing it. <br>
Risk: Deploying a Worker or widget to the wrong Cloudflare account can misconfigure production protection. <br>
Mitigation: Confirm the selected Cloudflare account and domains before irreversible widget creation or Worker deployment. <br>


## Reference(s): <br>
- [Canonical Turnstile Spin documentation](https://developers.cloudflare.com/turnstile/spin/) <br>
- [Cloudflare Turnstile client script](https://challenges.cloudflare.com/turnstile/v0/api.js) <br>
- [Cloudflare Turnstile reCAPTCHA migration](https://developers.cloudflare.com/turnstile/migration/recaptcha/) <br>
- [Cloudflare Pages Turnstile plugin](https://developers.cloudflare.com/pages/functions/plugins/turnstile/) <br>
- [Managed siteverify Worker](https://github.com/cloudflare/turnstile-siteverify) <br>
- [vanilla-html reference](references/vanilla-html.md) <br>
- [nextjs-app reference](references/nextjs-app.md) <br>
- [nextjs-pages reference](references/nextjs-pages.md) <br>
- [astro reference](references/astro.md) <br>
- [sveltekit reference](references/sveltekit.md) <br>
- [hugo reference](references/hugo.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON status handling, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces confirmation-driven steps, diffs for frontend edits, validation results, and a final setup summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
