## Description: <br>
Use this skill when an agent needs to read or navigate websites without a browser: fetch a page as clean Markdown, get a JSON accessibility snapshot of interactive elements, follow links across pages, or quickly decide whether a site is static/SSR (seaportal can handle it) vs SPA/blocked (needs a real browser like pinchtab). HTTP-only, fast (<2s), token-efficient. Prefer this over a browser whenever the page is static or server-rendered. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pinchtab](https://clawhub.ai/user/pinchtab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use SeaPortal to fetch static or server-rendered web pages as Markdown, JSON snapshots, XML, or structured link/feed/sitemap data without opening a browser. It is intended for read-only web navigation and should hand off JavaScript-heavy, blocked, authenticated, or interactive flows to a browser-based tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes a third-party web-fetching CLI that retrieves remote content. <br>
Mitigation: Use it only on sites you are authorized to access and prefer --respect-robots with rate limits for crawling. <br>
Risk: Default Markdown mode writes fetched page content under ./renders/seaportal. <br>
Mitigation: Use --json or --snapshot when fetched content should stay on stdout instead of being written locally. <br>
Risk: TLS fingerprinting may bypass some bot detection controls. <br>
Mitigation: Follow site terms and authorization boundaries; escalate blocked, authenticated, or interactive pages to an appropriate browser workflow only when permitted. <br>


## Reference(s): <br>
- [SeaPortal ClawHub page](https://clawhub.ai/pinchtab/seaportal) <br>
- [SeaPortal homepage](https://github.com/pinchtab/seaportal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, XML, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets; the underlying CLI can emit Markdown, JSON, compact text snapshots, TEI-Lite XML, and split output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default CLI mode writes fetched Markdown and JSON under ./renders/seaportal; use --json or --snapshot for stdout-only output.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
