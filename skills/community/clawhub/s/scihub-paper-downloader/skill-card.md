## Description: <br>
Get a PDF link from Sci-Hub for a DOI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aukaukauk](https://clawhub.ai/user/aukaukauk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to resolve a DOI into a direct PDF URL when a Sci-Hub-style mirror can locate the paper. It also helps agents report not-found, open-access fallback, mirror-error, and invalid-input outcomes clearly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries Sci-Hub-style mirrors for DOI lookups. <br>
Mitigation: Install it only when that behavior is intentional, and prefer official publisher or open-access sources when possible. <br>
Risk: Returned PDF and open-access links are untrusted third-party URLs. <br>
Mitigation: Treat returned links as untrusted and review them before opening, sharing, or using them in downstream workflows. <br>
Risk: Custom mirror configuration can route requests through unexpected services. <br>
Mitigation: Set SCIHUB_MIRRORS only to mirrors you trust. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aukaukauk/scihub-paper-downloader) <br>
- [Publisher profile](https://clawhub.ai/user/aukaukauk) <br>
- [Default Sci-Hub mirror: sci-hub.st](https://sci-hub.st) <br>
- [Default Sci-Hub mirror: sci-hub.ru](https://sci-hub.ru) <br>
- [Default Sci-Hub mirror: sci-hub.se](https://sci-hub.se) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text URL or status lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a direct PDF URL when found, or NOT_FOUND, OA_LINK, MIRROR_ERROR, or INVALID_INPUT status output.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
