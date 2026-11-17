## Description:

Build premium static landing pages with the Stomme/PolyTrader design system. Glass morphism, CSS custom properties, separated copy, responsive, Cloudflare Pages-ready. Use when building a website, landing page, marketing site, or product page. Produces static HTML/CSS/JS with no framework dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathanlindsay](https://clawhub.ai/user/jonathanlindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site builders use this skill to generate static marketing, landing, website, and product pages from provided content sources. It guides page structure, theming, validation scripts, Cloudflare Pages deployment assets, and build notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pre-push validation can execute project JavaScript during git push checks.

Mitigation: Review or replace require() and dynamic import() checks with parsing-only validation before enabling the hook.

Risk: The CI example installs Playwright without a pinned version.

Mitigation: Pin Playwright and related dependencies in a lockfile before using the validation workflow.

Risk: The skill includes multilingual and post-deploy checks that may not match every generated site.

Mitigation: Enable or adapt those checks only when they match the project locales, selectors, and deployment target.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonathanlindsay/skills/stomme-landing-page-builder)
- [Design System Reference](artifact/references/design-system.md)
- [Pre-push Check Template](artifact/references/pre-push-check-template.sh)
- [Live Validation Template](artifact/references/validate-live-template.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated static HTML, CSS, JavaScript, shell scripts, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces framework-free static site assets, validation scripts, git hook setup, CI validation guidance, and BUILD-NOTES.md deployment instructions.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
