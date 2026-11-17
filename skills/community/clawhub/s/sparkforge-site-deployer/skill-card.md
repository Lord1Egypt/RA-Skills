## Description:

Helps agents scaffold, check, and deploy static websites to Vercel, Netlify, or GitHub Pages, including configuration, custom-domain notes, and pre-deploy checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crispyangles](https://clawhub.ai/user/crispyangles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site builders use this skill to create and publish simple static HTML sites quickly, with checklist-driven checks for metadata, mobile viewport support, custom domains, and accidental client-side secret exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production deployment commands can publish immediately to the wrong account or expose unchecked files.

Mitigation: Review generated files before running deployment, confirm the Vercel CLI is authenticated to the intended account, and run the included secret-check step before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crispyangles/skills/sparkforge-site-deployer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTML, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment commands and pre-deploy checks for static-site releases.]

## Skill Version(s):

3.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
