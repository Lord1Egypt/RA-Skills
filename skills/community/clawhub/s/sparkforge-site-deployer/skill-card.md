## Description: <br>
Site Deployer helps agents scaffold and publish static websites to Vercel, Netlify, or GitHub Pages with deployment configuration, custom-domain guidance, Tailwind templates, and a pre-deploy checklist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Crispyangles](https://clawhub.ai/user/Crispyangles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and site owners use this skill to create static site files, configure deployment settings, check common launch issues, and publish a static site through Vercel, Netlify, or GitHub Pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a production deployment command that can publish a site to a live Vercel project. <br>
Mitigation: Review the generated files, confirm the target account and project, and consider a preview deploy or removing automatic confirmation before production deployment. <br>
Risk: Static site files can accidentally expose API keys or other secrets in public HTML or JavaScript. <br>
Mitigation: Run the included pre-deploy secret checks and manually review public assets before deploying. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline HTML, JSON configuration, and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces static-site scaffolding, deployment commands, DNS guidance, and pre-deploy checks for human review.] <br>

## Skill Version(s): <br>
3.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
