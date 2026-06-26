## Description: <br>
Build premium static landing pages with the Stomme/PolyTrader design system, including glass morphism, CSS custom properties, separated copy, responsive layouts, and Cloudflare Pages-ready static HTML, CSS, and JavaScript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonathanlindsay](https://clawhub.ai/user/jonathanlindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site builders use this skill to generate polished static marketing sites, landing pages, product pages, and supporting deployment assets from provided content sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated validation hooks, CI workflow steps, Playwright checks, and deployment URLs may be copied into an unintended repository or site. <br>
Mitigation: Review and adapt the generated Git hook, CI workflow, Playwright dependency, and live-validation URL before using the generated output. <br>
Risk: Generated landing pages may contain visual or interaction regressions such as low-contrast buttons, broken theme toggles, or cache-related asset issues. <br>
Mitigation: Run the generated pre-push and live validation scripts at desktop and mobile viewports before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jonathanlindsay/stomme-landing-page-builder) <br>
- [Design System Reference](references/design-system.md) <br>
- [Pre-push check template](references/pre-push-check-template.sh) <br>
- [Live validation template](references/validate-live-template.js) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Static HTML, CSS, JavaScript, shell scripts, configuration files, and Markdown deployment notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated sites separate copy into JavaScript data, include Cloudflare Pages assets, and include static and browser-based validation scripts.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
