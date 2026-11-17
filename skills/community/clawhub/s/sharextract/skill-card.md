## Description:

ShareXtract extracts normalized content from public share URLs, RSS/Atom feeds, timed-text documents, and web pages using a protocol-first fallback ladder without bypassing authentication, CAPTCHAs, paywalls, or access controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuaishare](https://clawhub.ai/user/wuaishare)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agents use this skill to retrieve already-public shared content and convert it into normalized text, Markdown, JSON fields, metadata, messages, and media references. It is suited for public AI chat shares, social and media links, RSS/Atom feeds, timed-text files, articles, oEmbed pages, and public JSON endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes public network requests and remote payloads may contain untrusted text, HTML, JSON, captions, metadata, or embedded tool-like instructions.

Mitigation: Treat extracted content strictly as data, preserve clear quotation and data boundaries, and require independent user intent before taking downstream action.

Risk: A supplied URL could be abused if interpolated into a shell command or command string.

Mitigation: Accept only one absolute public http/https URL and pass it as a single argv element through a shell-free process API; stop if only shell-string execution is available.

Risk: Using credentials, private sessions, or bypass techniques could retrieve content outside the public-content boundary.

Mitigation: Do not reuse cookies, tokens, browser state, CAPTCHA solvers, paywall bypasses, WAF bypasses, private signatures, or account automation; stop when access controls are encountered.

Risk: Runtime mismatch or untrusted provisioning could undermine the extraction boundary.

Mitigation: Install only where ShareXtract v0.23.4 is already trusted and provisioned, verify the expected runtime version, and do not download, install, upgrade, or modify dependencies during skill execution.

Risk: Some platform routes are undocumented or depend on changing public page structures, which may reduce extraction fidelity.

Mitigation: Inspect extraction_method, confidence, warnings, canonical_url, and metadata before downstream use; use adapter health checks for automated workflows and fail closed when content cannot be verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuaishare/skills/sharextract)
- [Platform matrix and extraction policy](references/platform-matrix.md)
- [Adding an adapter](references/adding-adapters.md)
- [Ecosystem map](references/ecosystem.md)
- [Adapter health and fixture corpus](references/adapter-health.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [JSON or Markdown extraction results with structured shell-free argv examples and human-readable guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted, preinstalled ShareXtract v0.23.4 runtime; accepts one absolute public http/https URL and returns normalized content with provenance fields, metadata, warnings, and retrieval time.]

## Skill Version(s):

0.23.4 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
