## Description:

Hreflang and international SEO audit, validation, and generation for detecting common mistakes, validating language and region codes, and generating correct hreflang implementations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners, developers, and site operators use this skill to audit international SEO implementations, validate hreflang and locale signals, and generate implementation-ready hreflang tags, headers, sitemap entries, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect user-provided URLs or local content directories while auditing hreflang and localization issues.

Mitigation: Review the target URLs and local paths before running an agent with this skill, and avoid sending sensitive or private content unless that review is acceptable.

Risk: Cultural adaptation and language-format findings are SEO heuristics and may not match every brand, audience, or target locale.

Mitigation: Have a qualified reviewer adapt recommendations to the actual market, audience, legal context, and brand voice before publishing changes.

Risk: Generated hreflang tags, headers, or sitemap entries can create misleading SEO signals if page equivalence, canonical URLs, or return tags are wrong.

Mitigation: Validate generated implementations against canonical URL maps and reciprocal hreflang sets before deploying to production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-hreflang)
- [Content Parity Audit](references/content-parity.md)
- [Cultural Adaptation Profiles](references/cultural-profiles.md)
- [Locale Format Reference](references/locale-formats.md)
- [Machine-translation QA flag](references/machine-translation-qa.md)
- [Google Search spam policies](https://developers.google.com/search/docs/essentials/spam-policies)
- [Google Search Quality Rater Guidelines](https://services.google.com/fh/files/misc/hsw-sqrg.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with implementation snippets, validation reports, tables, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HTML link tags, HTTP Link headers, XML sitemap examples, issue severity tables, and prioritized recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
