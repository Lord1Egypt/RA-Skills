## Description:

Converts a WordPress website to a static Cloudflare Pages site by mirroring rendered HTML, collecting referenced assets, fixing URLs, self-hosting fonts, stripping WordPress metadata, and deploying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhibavishi](https://clawhub.ai/user/abhibavishi)

### License/Terms of Use:


## Use Case:

Developers and site operators use this skill to convert an existing WordPress site into a static Cloudflare Pages deployment while preserving rendered pages, referenced assets, fonts, redirects, and cache configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell workflow could accidentally pull or publish sensitive server files.

Mitigation: Use a non-production SSH account limited to the target site, prefer allowlisted static assets over broad copies, and inspect ./public before any GitHub push or Cloudflare deployment.

Risk: SSH, rsync, git, and deployment commands depend on user-provided variables and remote paths.

Mitigation: Review command variables for safe quoting, validate all required environment variables and tools before execution, and stop on failed checks instead of retrying blindly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abhibavishi/skills/wp-to-static)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SSH, GitHub CLI, Cloudflare Wrangler, and WordPress connection environment variables.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
