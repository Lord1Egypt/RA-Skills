## Description:

Audits built website output and deployed URLs for technical SEO, GEO/AI visibility, and Core Web Vitals issues, then guides fixes using bundled hard-gate, structured-data, GEO, and LCP references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to audit rendered site output and deployed origins for SEO, AI crawler visibility, structured data, Core Web Vitals, and launch-readiness issues, then apply prioritized fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The live URL auditor can be used from the agent environment to probe internal or private web services if pointed at localhost, private IPs, cloud metadata addresses, or attacker-supplied URLs.

Mitigation: Run the local build-output audit by default; only run audit-live.mjs against public websites you control or trust until private-network blocking, redirect validation, request timeouts, and response-size limits are added.

Risk: CSP unsafe-inline style advice can be misapplied as a blanket production recommendation.

Mitigation: Treat unsafe-inline style allowances as explicit tradeoffs requiring security review before production use.

## Reference(s):

- [Hard Gates Reference](references/hard-gates.md)
- [Structured Data Reference](references/structured-data.md)
- [GEO AI Visibility Reference](references/geo-ai-visibility.md)
- [LCP Playbook](references/lcp-playbook.md)
- [Build-Time SEO Gates Case Study](analysis/case-study-build-time-seo-gates.md)
- [Source Homepage](https://github.com/Cosmofang/seo-audit)
- [ClawHub Skill Page](https://clawhub.ai/cosmofang/skills/seo-geo-gate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, code snippets, configuration guidance, and optional JSON audit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are printed to stdout; files are written only when the user redirects output.]

## Skill Version(s):

1.1.0 (source: evidence release, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
