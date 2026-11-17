## Description:

Report Expert helps agents convert HTML, Markdown, URLs, or text into structured HTML report pages and deploy them to Cloudflare Pages with linting and verification support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomtrije](https://clawhub.ai/user/tomtrije)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-producing agents use this skill to turn research or analysis material into publishable HTML report pages. It is suited for maintaining a Cloudflare Pages report site with generated indexes, static assets, deployment commands, and post-deployment verification guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL fetching and remote sync can import content from untrusted or unintended locations.

Mitigation: Review each source URL and only sync from the intended Cloudflare Pages site before publishing.

Risk: Cloudflare deployment commands can publish or overwrite site content.

Mitigation: Use a least-privilege Cloudflare API token scoped to one Pages project and verify the project name before deployment.

Risk: Untrusted HTML or Markdown may contain unsafe or misleading content even when structural linting runs.

Mitigation: Sanitize or manually review untrusted report content before allowing the skill to publish it.

Risk: Deployment environments can expose broad secrets to the process.

Mitigation: Run with only the Cloudflare and report-site environment values needed for the release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tomtrije/skills/report-expert)
- [Publisher Profile](https://clawhub.ai/user/tomtrije)
- [Manifest Repository URL](https://report-expert-skill.pages.dev)
- [Deployment Checklist](references/checklist.md)
- [Verification Detail](references/verify-detail.md)
- [Chart Specification](references/chart-spec.md)
- [Design Specification](references/design-spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands plus generated HTML, CSS, JavaScript, and JSON site files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local report inputs, fetch source URLs, write dist files, synchronize static assets, and publish to a configured Cloudflare Pages project.]

## Skill Version(s):

2.0.0 (source: target metadata, release evidence, and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
