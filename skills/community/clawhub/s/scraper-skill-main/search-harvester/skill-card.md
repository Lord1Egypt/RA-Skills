## Description: <br>
ScrapeBox-style candidate discovery for link building and outreach. Rotates Tor exit nodes (and optionally public HTTP proxies) so the server's datacenter IP never touches the search engine, harvests candidate URLs from multiple engines (DuckDuckGo HTML, Marginalia), dedupes, triages liveness/anti-bot barriers, and exports a scored candidate list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toniilic](https://clawhub.ai/user/toniilic) <br>

### License/Terms of Use: <br>
MIT-0 <br>

## Use Case: <br>
SEO practitioners, link builders, founders, and marketers use this skill to discover directories, submission platforms, blogs, and listicles to submit their site or client sites to — without getting the source server IP banned by search engines. It replaces manual SERP scraping that hits captcha walls from datacenter IPs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes HTTP traffic through the Tor network, which changes the visible source IP and may trigger additional security checks on some sites. <br>
Mitigation: Use the included rotate-and-retry loop (NEWNYM) to find clean exit nodes; the skill treats 403/429 as retry signals, not results. <br>
Risk: Public proxy lists are unreliable and some proxies may be slow or malicious. <br>
Mitigation: Tor is the primary transport; public HTTP proxies are only a documented fallback, and harvested results are triaged for liveness before use. <br>
Risk: Automated search-engine queries may violate a search engine's terms of service. <br>
Mitigation: The skill is designed for low-volume, rate-limited discovery; users should review local law and each engine's ToS before deployment. <br>

## Reference(s): <br>
OpenClaw docs — Skill format: https://docs.openclaw.ai/clawhub/skill-format <br>
OpenClaw docs — Publishing: https://docs.openclaw.ai/clawhub/publishing <br>

## Skill Output: <br>
**Output Type(s):** [Markdown, Text, JSON] <br>
**Output Format:** [Ranked markdown candidate list with URL, title, liveness status, barrier type, and suggested action; optionally a JSON report and an interactive markdown export.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Tor instance (SOCKSPort 127.0.0.1:19050 + ControlPort 127.0.0.1:19051); includes a Python 3 script (stdlib only) that shells out to curl; requires tor, curl, python3, nc binaries; does not read local project context files or send harvested data anywhere except the search engines queried.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. Automated scraping may be subject to search-engine terms of service and local regulations; use at low volume and rate-limited cadence. <br>
