## Description: <br>
Creates, rebuilds, publishes, and operates Notion-managed websites, including CMS sections, widgets, search and filtering interactions, SEO improvements, validation, and lightweight deployment workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollaugo](https://clawhub.ai/user/hollaugo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, site operators, and developers use this skill to create or rebuild websites, model Notion-managed content, add searchable listings and widgets, validate pages, and publish through lightweight hosting workflows such as Netlify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notion and Netlify credentials may be used for CMS setup, synchronization, or deployment workflows. <br>
Mitigation: Provide narrowly scoped tokens only when those workflows are requested, and avoid supplying credentials for planning, blueprinting, or validation-only tasks. <br>
Risk: The skill may write local .website-manager JSON files containing non-secret site, CMS, or deployment metadata. <br>
Mitigation: Review those files before committing or syncing them, and keep them local unless the project intentionally tracks that metadata. <br>
Risk: Automated deployment can publish website changes to Netlify. <br>
Mitigation: Validate generated pages and links before deploy, and use the least-privileged Netlify token that can deploy to the intended site or account. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/hollaugo/website-manager) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills) <br>
- [Default Stack](references/default-stack.md) <br>
- [Notion CMS Model](references/notion-cms-model.md) <br>
- [Hosting Decision Guide](references/hosting-decision.md) <br>
- [SEO / AEO / GEO Reference](references/seo-aeo-geo.md) <br>
- [Widgets and Interactions](references/widgets-and-interactions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code, shell commands, JSON configuration, and generated website files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local non-secret .website-manager JSON metadata and may call Notion or Netlify APIs only when credentials are provided for those workflows.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
