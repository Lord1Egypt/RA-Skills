## Description: <br>
TinyScraper helps an agent mirror a simple static website by downloading same-domain HTML, JavaScript, CSS, and static assets for offline browsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alukardo](https://clawhub.ai/user/alukardo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use TinyScraper when asked to download, mirror, or offline-save a simple static website. It is best suited to same-domain static pages and assets, with dry-run support for previewing crawl scope before downloading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup command can recursively delete paths built from unvalidated user input. <br>
Mitigation: Use TinyScraper only in a sandbox or disposable workspace and avoid cleanup with manually supplied or untrusted domain values until the publisher validates deletion stays inside the mirror directory. <br>
Risk: Mirroring a site can download content beyond the intended scope or from sites the user is not authorized to crawl. <br>
Mitigation: Run dry-run first, set crawl limits where possible, and crawl only sites the user is allowed to mirror. <br>


## Reference(s): <br>
- [TinyScraper Format Specification](references/SPEC.md) <br>
- [ClawHub TinyScraper Release Page](https://clawhub.ai/alukardo/tiny-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local mirrored website files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces crawl progress logs and writes mirrored content under tmp/mirrors/{domain}.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
