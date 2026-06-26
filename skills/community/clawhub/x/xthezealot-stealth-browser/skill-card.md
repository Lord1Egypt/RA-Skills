## Description: <br>
Access websites with advanced bot protection to fetch HTML, screenshots, PDFs, or multiple pages in parallel using isolated browser contexts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xthezealot](https://clawhub.ai/user/xthezealot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to retrieve page HTML, screenshots, PDFs, or multiple page summaries from sites that may challenge automated browsers. Use should be limited to authorized browsing and testing contexts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary reports a command-injection flaw and unvalidated URL handling. <br>
Mitigation: Use only in a controlled sandbox for authorized testing until command execution is changed to argument-array process execution and URL validation is added. <br>
Risk: The server security summary reports automatic install behavior when the skill is loaded. <br>
Mitigation: Review and preinstall dependencies in an isolated environment; remove automatic npm install-on-load before normal deployment. <br>
Risk: The server security guidance calls out disabled browser sandboxing and anti-bot evasion behavior. <br>
Mitigation: Restore browser sandboxing where possible and document clear limits against unauthorized anti-bot evasion. <br>
Risk: The skill can save screenshots and PDFs to local temporary paths. <br>
Mitigation: Document generated artifacts and clean up saved files after review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xthezealot/xthezealot-stealth-browser) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files] <br>
**Output Format:** [Plain text or formatted Markdown; parallel browsing returns JSON-derived summaries; screenshot and PDF commands save files and return their paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [HTML output may be truncated by the wrapper; generated screenshots and PDFs are timestamped files under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
